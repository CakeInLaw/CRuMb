from enum import Enum
from typing import TYPE_CHECKING, Generic, TypeVar, Type, TypedDict, Literal, Any, Optional, Coroutine, Callable, \
    overload, cast, Sequence
from uuid import UUID

from pydantic.error_wrappers import ValidationError
from tortoise import models, fields
from tortoise.queryset import QuerySet
from tortoise.transactions import in_transaction

from .base_model import BaseModel
from .exceptions import ItemNotFound, ObjectErrors, UnexpectedDataKey, FieldError, NotUnique, NotUniqueTogether, \
    FieldRequired, NotFoundFK, RequiredMissed, InvalidType, AnyFieldError, NoDefaultRepository, ListFieldError
from .filters import Filter
from .enums import FieldTypes
from .maps import field_instance_to_type

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin


T = TypeVar('T')
MODEL = TypeVar('MODEL', bound=Type[BaseModel])
PK = TypeVar('PK', int, str, UUID)
SORT = list[str]
FILTERS = list[Filter]
DATA = dict[str, Any]
FK_TYPE = fields.IntField | fields.SmallIntField | fields.BigIntField |\
          fields.UUIDField | fields.CharField | fields.Field


class SortedData(TypedDict):
    db_field: dict[str, Any]
    o2o: dict[str, DATA]
    o2o_pk: dict[str, int | BaseModel]
    fk: dict[str, DATA]
    fk_pk: dict[str, int | BaseModel]
    back_o2o: dict[str, DATA]
    back_fk: dict[str, list[DATA]]
    m2m: dict[str, list[PK]]


class RepositoryDescription(TypedDict):
    _all: dict[str, FieldTypes]
    db_field: dict[str, fields.Field]
    o2o: dict[str, fields.relational.OneToOneFieldInstance]
    o2o_pk: dict[str, FK_TYPE]
    fk: dict[str, fields.relational.ForeignKeyFieldInstance]
    fk_pk: dict[str, FK_TYPE]
    back_o2o: dict[str, fields.relational.BackwardOneToOneRelation]
    back_fk: dict[str, fields.relational.BackwardFKRelation]
    m2m: dict[str, fields.relational.ManyToManyFieldInstance]


class AdminRepositoryExtra(TypedDict):
    app: Type["CRuMbAdmin"]


class Repository(Generic[MODEL, PK]):
    model: Type[MODEL]

    by: str
    extra: dict[str, Any]
    select_related: tuple[str]
    prefetch_related: tuple[str]

    def __init__(
            self,
            by: str = '',
            extra: dict[str, Any] = None,
            select_related: tuple[str] = (),
            prefetch_related: tuple[str] = (),
    ):
        self.by = by
        self.extra = extra or {}
        self.select_related = select_related
        self.prefetch_related = prefetch_related

    def get_queryset(self):
        query = self.model.all()
        if default_filters := self.qs_default_filters():
            query = query.filter(**default_filters)
        if annotate_fields := self.qs_annotate_fields():
            query = query.annotate(**annotate_fields)
        if final_select_related := {*self.qs_select_related(), *self.select_related}:
            query = query.select_related(*final_select_related)
        if final_prefetch_related := {*self.qs_prefetch_related(), *self.prefetch_related}:
            query = query.prefetch_related(*final_prefetch_related)
        return query

    def qs_default_filters(self) -> dict[str, Any]:
        return {}

    def qs_annotate_fields(self) -> dict[str, Any]:
        return {}

    def qs_select_related(self) -> set[str]:
        return set()

    def qs_prefetch_related(self) -> set[str]:
        return set()

    @classmethod
    def opts(cls) -> models.MetaInfo:
        return cls.model._meta

    @property
    def pk_field_type(self) -> Type[PK]:
        return self.opts().pk.field_type  # type: ignore

    @property
    def pk_attr(self) -> str:
        return self.opts().pk_attr

    async def get_all(
            self,
            skip: Optional[int],
            limit: Optional[int],
            sort: SORT,
            filters: FILTERS,
    ) -> tuple[list[MODEL], int]:
        query = self.get_queryset()
        for f in filters:
            query = f.filter(query)
        base_query = query
        if sort:
            query = query.order_by(*sort)
        if skip:
            query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        async with in_transaction():
            result = await query
            count = await base_query.count()
        return result, count

    def _get_many_queryset(self, item_pk_list: list[PK]) -> QuerySet[MODEL]:
        return self.get_queryset().filter(pk__in=item_pk_list)

    async def get_many(self, item_pk_list: list[PK]) -> list[MODEL]:
        return await self._get_many_queryset(item_pk_list)

    @overload
    async def get_one(self, value: PK) -> Optional[MODEL]: ...

    @overload
    async def get_one(self, value: Any, *, field_name: str) -> Optional[MODEL]: ...

    async def get_one(self, value, *, field_name='pk') -> Optional[MODEL]:
        if field_name in self.model.IEXACT_FIELDS:
            field_name = field_name + '__iexact'
        instance = await self.get_queryset()\
            .get_or_none(**{field_name: value})
        if instance is None:
            raise ItemNotFound()
        return instance

    async def create(
            self,
            data: DATA,
            *,
            defaults: Optional[DATA] = None,
            is_root: bool = True,
    ) -> MODEL:
        """
        :param data: Данные для вставки в БД, которые соответствуют её структуре. Метод transform_data позволяет
                     изменить передаваемые данные ТОЛЬКО В КОРНЕВОМ вызове Repository.create.
        :param defaults: Данные, которые вставляются по умолчанию БЕЗ ПРОВЕРКИ. Используется, например, чтобы
                         установить ссылку на ntreobq объект, создавая back_o2o или back_fk
        :param is_root: явно указывает находимся ли мы в корне или функция create вызвана другим Repository.create
        """
        if is_root:
            data = await self.transform_data(data)
            await self.validate(data)

        async def get_new_instance() -> MODEL:
            direct_related = {}
            sorted_data: SortedData = self.sort_data_by_field_types(data)

            for t in ('o2o', 'fk'):
                t: Literal["o2o", "fk"]
                for field_name, value in sorted_data[t]:
                    direct_related[field_name] = await self.repository_of(field_name)(
                        by=f'{self.by}__{self.model.__name__}',
                        extra=self.extra
                    ).create(value, is_root=False)

            for t in ('o2o_pk', 'fk_pk'):
                t: Literal["o2o_pk", "fk_pk"]
                for field_name, value in sorted_data[t].items():
                    # при валидации мы убедились, что запись в бд есть, поэтому просто подвязываем по первичному ключу
                    if isinstance(value, BaseModel):
                        direct_related[field_name] = value.pk
                    else:
                        direct_related[field_name] = value

            instance = await self.model.create(**{
                **(defaults or {}),
                **sorted_data['db_field'],
                **direct_related
            })

            for field_name, value in sorted_data['back_o2o'].items():
                relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                await self.repository_of(field_name)(
                    by=f'{self.by}__{self.model.__name__}',
                    extra=self.extra
                ).create(value, defaults={relation_field: instance.pk}, is_root=False)

            for field_name, value in sorted_data['back_fk'].items():
                relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                for v in value:
                    await self.repository_of(field_name)(
                        by=f'{self.by}__{self.model.__name__}',
                        extra=self.extra
                    ).create(v, defaults={relation_field: instance.pk}, is_root=False)

            for field_name, values in sorted_data['m2m'].items():
                await self.save_m2m(
                    instance,
                    field_name,
                    values,
                    method='add',
                )

            return instance

        if is_root:
            async with in_transaction():
                new_instance = await get_new_instance()
                await self.post_create(new_instance)
                return await self.get_one(new_instance.pk)
        else:
            return await get_new_instance()

    async def post_create(self, new_instance: MODEL) -> None:
        """Override this function"""
        pass

    async def save_m2m(
            self,
            instance: MODEL,
            field_name: str,
            values: Sequence[PK],
            *,
            method: Literal['add', 'delete', 'clear'] = 'add'
    ) -> None:
        rel: fields.relational.ManyToManyRelation = getattr(instance, field_name)
        field: fields.relational.ManyToManyFieldInstance = self.get_field_instance(field_name)  # type: ignore
        if method == 'clear':
            await rel.clear()
            if values:
                instances = await field.related_model.filter(pk__in=values)
                await rel.add(*instances)
        elif method == 'delete':
            if values:
                instances = await field.related_model.filter(pk__in=values)
                if instances:
                    await rel.remove(*instances)
        elif method == 'add':
            if values:
                instances = await field.related_model.filter(pk__in=values)
                await rel.add(*instances)
        else:
            raise ValueError(f'Неизвестный метод `{method}`')

    async def delete_many(self, item_pk_list: list[PK]) -> int:
        raise NotImplementedError('Для этой модели не определено множественное удаление')

    async def delete_one(self, instance: MODEL) -> None:
        raise NotImplementedError('Для этой модели не определено удаление')

    async def check_fk_exists(self, field_name: str, item_pk: PK) -> None:
        field_type = self.get_field_type(field_name)
        field = self.get_field_instance(field_name)

        if field_type in (FieldTypes.O2O, FieldTypes.FK):
            related_field = cast(fields.relational.ForeignKeyFieldInstance, field)
        elif field_type in (FieldTypes.O2O_PK, FieldTypes.FK_PK):
            related_field = cast(fields.relational.ForeignKeyFieldInstance, field.reference)
        else:
            raise Exception(f'{self.model}.{field_name} не относится к o2o, o2o_pk, fk, fk_pk или m2m')
        if not await related_field.related_model.exists(pk=item_pk):
            raise NotFoundFK

    async def check_unique(
            self,
            field_name: str,
            value: Any,
            data: DATA,
            instance: Optional[MODEL] = None,
    ) -> None:
        if await self.model.exists(**{field_name: value}):
            raise NotUnique

    async def check_unique_together(
            self,
            data: DATA,
            instance: Optional[MODEL] = None
    ) -> None:
        """Недоделано"""
        errors = ObjectErrors()
        for combo in self.opts().unique_together:
            values = {}
            # if instance:
            for field_name in combo:
                # field = self.get_field_instance(field_name)
                # :) посмотри какие именно значения добавляются в unique_together, если пишешь туда o2o и fk
                raise NotImplementedError
            if await self.model.exists(**values):
                errors.root = NotUniqueTogether(combo)
        if errors:
            raise errors

    async def transform_data(self, data: DATA, *, instance: Optional[MODEL] = None) -> DATA:
        return data

    @classmethod
    def sort_data_by_field_types(cls, data: DATA) -> SortedData:
        _all_fields: dict[str, FieldTypes] = cls.describe()['_all']
        sorted_data = SortedData(
            db_field={},
            o2o={},
            o2o_pk={},
            fk={},
            fk_pk={},
            back_o2o={},
            back_fk={},
            m2m={},
        )
        for key, value in data.items():
            if key not in _all_fields:
                raise UnexpectedDataKey(f'Unexpected key `{key}` in model `{cls.model}`')
            field_type = _all_fields[key].value
            if field_type in sorted_data.keys():
                sorted_data[field_type][key] = value  # type: ignore
            else:
                sorted_data['db_field'][key] = value
        return sorted_data

    async def validate(self, data: DATA, instance: Optional[MODEL] = None) -> None:
        errors = ObjectErrors()

        required, pairs = self.required_and_pairs()
        required = required if instance is None else {}

        sorted_data: SortedData = self.sort_data_by_field_types(data)

        for t in SortedData.__annotations__.keys():
            for name, value in sorted_data[t].items():  # type: ignore
                if name in required:
                    related = required[name]
                    del required[name]
                    if related:
                        del required[related]
                if name in pairs:
                    if pairs[name] not in pairs:
                        raise Exception(f'{name} и {pairs[name]} были переданы одновременно')
                    del pairs[name]
                try:
                    await self.validate_field(
                        name, value, data, instance, default_validator=getattr(self, f'validate_{t}')
                    )
                except ObjectErrors as e:
                    errors.merge(e)

        for name, related in required.items():
            errors.root = RequiredMissed(name, related)
        if errors:
            raise errors

    def validate_field(
            self,
            field_name: str,
            value: T,
            data: DATA,
            instance: Optional[MODEL],
            default_validator: Callable[[str, T, DATA, Optional[MODEL]], Coroutine[Any, Any, None]]
    ) -> Optional[Coroutine[Any, Any, None]]:
        return getattr(self, f'_validate_{field_name}', default_validator)(field_name, value, data, instance)

    async def validate_relational(
            self,
            field_name: str,
            value: DATA,
            data: DATA,
            instance: Optional[MODEL]
    ):
        if instance:
            rel_instance = getattr(instance, field_name)
            if not isinstance(rel_instance, BaseModel):
                await instance.fetch_related(field_name)
                rel_instance = getattr(instance, field_name)
        else:
            rel_instance = None
        await self.repository_of(field_name)(
            by=f'{self.by}__{self.model.__name__}',
            extra=self.extra
        ).validate(value, rel_instance)

    async def validate_o2o(
            self,
            field_name: str,
            value: DATA,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        if not isinstance(data, dict):
            raise InvalidType(f'o2o `{self.model}.{field_name}` data must be dict, not {type(value)} ({value})')
        await self.validate_relational(field_name, value, data, instance)

    async def validate_o2o_pk(
            self,
            field_name: str,
            value: int | BaseModel,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        field = self.get_field_instance(field_name)
        reference = cast(fields.relational.OneToOneFieldInstance, field.reference)

        if value is None and not field.null:
            raise FieldRequired

        if isinstance(value, field.field_type):  # передали правильный тип pk
            item_pk = value
        elif isinstance(value, reference.related_model):  # передали инстанс правильной модели
            item_pk = value.pk
        else:
            raise InvalidType(
                f'o2o_pk `{self.model}.{field_name}` data must be int | {reference.related_model}, '
                f'not {type(value)} ({value})'
            )
        try:
            await self.check_unique(field_name, item_pk, data, instance)
            await self.check_fk_exists(field_name, item_pk)  # type: ignore
        except FieldError as e:
            raise ObjectErrors().add(field_name, e)

    async def validate_fk(
            self,
            field_name: str,
            value: DATA,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        if not isinstance(value, dict):
            raise InvalidType(f'fk `{self.model}.{field_name}` data must be dict, not {type(value)} ({value})')
        await self.validate_relational(field_name, value, data, instance)

    async def validate_fk_pk(
            self,
            field_name: str,
            value: int | BaseModel,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        field = self.get_field_instance(field_name)
        reference = cast(fields.relational.ForeignKeyFieldInstance, field.reference)

        if value is None and not field.null:
            raise FieldRequired

        if isinstance(value, field.field_type):  # передали правильный тип pk
            item_pk = value
        elif isinstance(value, reference.related_model):  # передали инстанс правильной модели
            item_pk = value.pk
        else:
            raise InvalidType(
                f'fk_pk `{self.model}.{field_name}` data must be int | {reference.related_model}, '
                f'not {type(value)} ({value})'
            )
        try:
            await self.check_fk_exists(field_name, item_pk)  # type: ignore
        except FieldError as e:
            raise ObjectErrors().add(field_name, e)

    async def validate_back_o2o(
            self,
            field_name: str,
            value: DATA,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        if not isinstance(value, dict):
            raise InvalidType(f'back_o2o `{self.model}.{field_name}` data must be dict, not {type(value)} ({value})')
        await self.validate_relational(field_name, value, data, instance)

    async def validate_back_fk(
            self,
            field_name: str,
            value: Sequence[DATA],
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        if not isinstance(value, Sequence) and all(isinstance(v, dict) for v in value):
            raise InvalidType(
                f'back_fk `{self.model}.{field_name}` data must be list[dict], not {type(value)} ({value})'
            )
        list_error = ListFieldError()
        for i, v in enumerate(value):
            try:
                await self.validate_relational(field_name, v, data, instance)
            except ObjectErrors as err:
                list_error.append(i, err=err)
        if list_error:
            raise ObjectErrors().add(field_name, list_error)

    async def validate_m2m(
            self,
            field_name: str,
            value: Sequence[PK],
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        field: fields.relational.ManyToManyFieldInstance = self.get_field_instance(field_name)  # type:ignore
        pk_field_type = field.related_model._meta.pk.field_type
        if not (
                isinstance(value, Sequence)
                and not isinstance(value, str)
                and all(isinstance(v, pk_field_type) for v in value)
        ):
            raise InvalidType(
                f'back_fk `{self.model}.{field_name}` data must be Sequence[dict], not {type(value)} ({value})'
            )


    async def validate_db_field(
            self,
            field_name: str,
            value: Any,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        field = self.get_field_instance(field_name)
        if value is None and not field.null:
            raise FieldRequired
        if field.generated:
            raise UnexpectedDataKey
        if not isinstance(value, field.field_type):
            raise InvalidType(f'{self.model}.{field_name} data must be instance of {field.field_type}, '
                              f'not {type(value)} ({value})')
        if field.unique:
            await self.check_unique(field_name, value, data, instance)
        # позаимствовал кусок из field.validate(value) за исключением последней строки
        for v in field.validators:
            if field.null and value is None:
                continue
            try:
                if isinstance(value, Enum):
                    v(value.value)
                else:
                    v(value)
            except ValidationError as exc:
                raise AnyFieldError('invalid', str(exc))

    @classmethod
    def describe(cls) -> RepositoryDescription:
        if not hasattr(cls, '_describe_result'):
            description = RepositoryDescription(
                _all={},
                db_field={},
                o2o={},
                o2o_pk={},
                fk={},
                fk_pk={},
                back_o2o={},
                back_fk={},
                m2m={},
            )
            opts = cls.opts()

            for name in opts.o2o_fields:
                field = cast(models.OneToOneFieldInstance, opts.fields_map[name])
                description['o2o'][name] = field
                description['_all'][name] = FieldTypes.O2O
                description['o2o_pk'][field.source_field] = opts.fields_map[field.source_field]
                description['_all'][field.source_field] = FieldTypes.O2O_PK

            for name in opts.fk_fields:
                field = cast(models.ForeignKeyFieldInstance, opts.fields_map[name])
                description['fk'][name] = field
                description['_all'][name] = FieldTypes.FK
                description['fk_pk'][field.source_field] = opts.fields_map[field.source_field]
                description['_all'][field.source_field] = FieldTypes.FK_PK

            for name in opts.backward_o2o_fields:
                description['back_o2o'][name] = cast(fields.relational.BackwardOneToOneRelation, opts.fields_map[name])
                description['_all'][name] = FieldTypes.BACK_O2O

            for name in opts.backward_fk_fields:
                description['back_fk'][name] = cast(fields.relational.BackwardFKRelation, opts.fields_map[name])
                description['_all'][name] = FieldTypes.BACK_FK

            for name in opts.m2m_fields:
                description['m2m'][name] = cast(fields.relational.ManyToManyFieldInstance, opts.fields_map[name])
                description['_all'][name] = FieldTypes.M2M

            for name in opts.db_fields:
                if name not in description['_all']:
                    description['db_field'][name] = field = opts.fields_map[name]
                    description['_all'][name] = field_instance_to_type[field.__class__]

            setattr(cls, '_describe_result', description)
        return getattr(cls, '_describe_result')

    @classmethod
    def get_field_type(cls, field_name: str) -> FieldTypes:
        return cls.describe()["_all"][field_name]

    @classmethod
    def get_field_instance(cls, field_name: str) -> fields.Field:
        field_type = cls.get_field_type(field_name)
        # если это o2o, o2o_pk, fk, fk_pk, back_o2o, back_fk, m2m, иначе int, str, bool итд, которые падают в db_field
        if field_type.value in RepositoryDescription.__annotations__.keys():
            return cls.describe()[field_type.value][field_name]  # type: ignore
        return cls.describe()['db_field'][field_name]

    @classmethod
    def field_is_required(cls, field: fields.Field) -> bool:
        if isinstance(field, (fields.DatetimeField, fields.TimeField)) and (field.auto_now or field.auto_now_add):
            return False
        if field.required:
            return True
        return False

    @classmethod
    def required_and_pairs(cls) -> tuple[dict[str, Optional[str]], dict[str, str]]:
        """
        Возвращает заранее просчитанную копию обязательных полей и пар o2o с o2o_pk и fk с fk_pk
        Ключ - это поле, значение - это связанное поле. {"name": None, "user_id": "user", "user": "user_id"}
        У pairs только пары. Это нужно, чтобы определять, например, что передали одновременно и user, и user_id
        """
        if not hasattr(cls, '__required_and_pairs'):
            describe = cls.describe()
            required = {}
            pairs = {}
            for name, field in describe['db_field'].items():
                if cls.field_is_required(field):
                    required[name] = None
            for name, field in {**describe['o2o'], **describe['fk']}.items():
                if cls.field_is_required(field):
                    required[name] = field.source_field
                    pairs[name] = field.source_field
            for name, field in {**describe['o2o_pk'], **describe['fk_pk']}.items():
                if cls.field_is_required(field):
                    required[name] = field.reference.model_field_name
                    pairs[name] = field.reference.model_field_name
            setattr(cls, '__required_and_pairs', (required, pairs))
        required, pairs = getattr(cls, '__required_and_pairs')
        return {**required}, {**pairs}

    @classmethod
    @overload
    def repository_of(cls, field_name: str) -> Type["Repository"]: ...

    @classmethod
    @overload
    def repository_of(cls, field_name: str, *, raise_if_none: bool = True) -> Optional[Type["Repository"]]: ...

    @classmethod
    def repository_of(cls, field_name, *, raise_if_none = True) -> Optional[Type["Repository"]]:
        field = cls.get_field_instance(field_name)
        if isinstance(field, fields.relational.RelationalField):
            related_model = field.related_model
            default_repo: Type["Repository"] = getattr(related_model, 'DEFAULT_REPOSITORY', None)
            if default_repo is None and raise_if_none:
                raise NoDefaultRepository(
                    f'У поля {cls.model}.{field_name} ({related_model}) нет репозитория по умолчанию'
                )
            return default_repo
        raise NoDefaultRepository(
            f'Поле {cls.model}.{field_name} с типом {cls.get_field_type(field_name)} не может иметь репозиторий'
        )

REPOSITORY = TypeVar('REPOSITORY', bound=Type[Repository])


def default_repository(cls: REPOSITORY) -> REPOSITORY:
    """
    Декоратор, который устанавливает в класс модели репозиторий как дефолтный, чтобы другие репозитории могли
    пользоваться им для создания и редактирования вложенных моделей

    @default_repository
    class NomenclatureRepository(Repository):
        model = Nomenclature
        ...
    """

    cls.model.DEFAULT_REPOSITORY = cls
    return cls
