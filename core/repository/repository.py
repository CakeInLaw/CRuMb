from enum import Enum
from typing import Generic, TypeVar, Type, Literal, Any, Optional, Coroutine, Callable, overload, cast

from tortoise import models, fields
from tortoise.queryset import QuerySet
from tortoise.transactions import in_transaction
from tortoise.exceptions import ValidationError

from core.orm.base_model import BaseModel
from core.constants import EMPTY_TUPLE, UndefinedValue
from core.exceptions import ItemNotFound, ObjectErrors, UnexpectedDataKey, FieldError, NotUnique, \
    FieldRequired, NotFoundFK, RequiredMissed, InvalidType, AnyFieldError, ListFieldError
from core.enums import FieldTypes
from core.maps import field_instance_to_type
from core.translations import BaseTranslation

from core.types import MODEL, PK, SORT, FILTERS, DATA, SortedData, RepositoryDescription, BackFKData


T = TypeVar('T')
descriptions = {}


class Repository(Generic[MODEL]):
    model: Type[MODEL]

    READ_ONLY_REPOSITORY = False
    _REPOSITORY_NAME: str = '__default__'
    hidden_fields: set[str] = set()
    extra_allowed: set[str] = set()
    calculated: dict[str, FieldTypes] = dict()  # заменить на mutable?
    related_repositories: dict[str, str] = dict()  # заменить на mutable?

    _TRANSLATION_DEFAULT: BaseTranslation

    def __init__(
            self,
            by: str = '',
            extra: dict[str, Any] = None,
            instance: MODEL = None,
            select_related: tuple[str] = EMPTY_TUPLE,
            prefetch_related: tuple[str] = EMPTY_TUPLE,
    ):
        self.by = by
        self.extra = extra or {}
        self.instance = instance
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

    async def handle_create(
            self,
            data: DATA,
            extra_data: DATA
    ) -> MODEL:
        return await self.model.create(**data)

    async def get_create_defaults(self, data: DATA, user_defaults: Optional[DATA]) -> DATA:
        return user_defaults or {}

    def raise_if_read_only_repository(self):
        if self.READ_ONLY_REPOSITORY:
            raise Exception(f'{self} is read_only')

    async def create(
            self,
            data: DATA,
            *,
            defaults: Optional[DATA] = None,
            is_root: bool = True,
            run_in_transaction: Optional[bool] = None,
            validate: Optional[bool] = None,
    ) -> MODEL:
        """
        :param data: Данные для вставки в БД, которые соответствуют её структуре.
                     После передачи в функцию данные никак не изменяются.
        :param defaults: Данные, которые вставляются по умолчанию БЕЗ ПРОВЕРКИ. Используется, например, чтобы
                         установить ссылку на ntreobq объект, создавая back_o2o или back_fk
        :param is_root: Явно указывает находимся ли мы в корне или функция create вызвана другим Repository.create
        :param run_in_transaction: По умолчанию равно параметру is_root.
                                   Указывает нужно ли помещать вызов функции в транзакцию. Если функция уже находится в
                                   транзации, то новый контекст транзакции сломает отлов ошибки и собъет connection.
        :param validate: По умолчанию равно параметру is_root.
                         Стоит вручную передавать False, если передаются валидированные данные. Автоматически False
                         передается вместе с is_root, когда Repository.create вызывается из другой функции.
        """
        self.raise_if_read_only_repository()

        validate = is_root if validate is None else validate
        run_in_transaction = is_root if run_in_transaction is None else run_in_transaction

        if validate:
            await self.validate(data)

        async def get_new_instance() -> MODEL:
            direct_related = {}
            sorted_data: SortedData = self.sort_data_by_field_types(data)

            for t in ('o2o', 'fk'):
                t: Literal["o2o", "fk"]
                for field_name, value in getattr(sorted_data, t).items():
                    direct_related[field_name] = await self.repository_of(field_name)(
                        by=f'{self.by}__{self.model.__name__}',
                        extra=self.extra
                    ).create(value, is_root=False)

            for t in ('o2o_pk', 'fk_pk'):
                t: Literal["o2o_pk", "fk_pk"]
                for field_name, value in getattr(sorted_data, t).items():
                    # при валидации мы убедились, что запись в бд есть, поэтому просто подвязываем по первичному ключу
                    direct_related[field_name] = value

            result_defaults = await self.get_create_defaults(data, defaults)
            instance = await self.handle_create(
                data={**result_defaults, **sorted_data.db_field, **direct_related},
                extra_data=sorted_data.extra
            )

            for field_name, value in sorted_data.back_o2o.items():
                relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                await self.repository_of(field_name)(
                    by=f'{self.by}__{self.model.__name__}',
                    extra=self.extra
                ).create(value, defaults={relation_field: instance.pk}, is_root=False)

            for field_name, bfk_data in sorted_data.back_fk.items():
                relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                for value in bfk_data:
                    await self.repository_of(field_name)(
                        by=f'{self.by}__{self.model.__name__}',
                        extra=self.extra
                    ).create(value, defaults={relation_field: instance.pk}, is_root=False)

            await self.post_create(instance)
            return instance

        if run_in_transaction:
            async with in_transaction():
                new_instance = await get_new_instance()
                return await self.get_one(new_instance.pk)
        else:
            return await get_new_instance()

    async def post_create(self, new_instance: MODEL) -> None:
        """Override this function"""
        pass

    async def handle_edit(
            self,
            instance: MODEL,
            data: DATA,
            extra_data: DATA
    ):
        instance.update_from_dict(data)
        await instance.save(force_update=True)

    async def edit(
            self,
            instance: MODEL,
            data: DATA,
            *,
            defaults: Optional[DATA] = None,
            is_root: bool = True,
            run_in_transaction: Optional[bool] = None,
            validate: Optional[bool] = None,
    ) -> MODEL:
        """
        :param instance: Существующий объект модели для изменения.
        :param data: Данные для вставки в БД, которые соответствуют её структуре.
                     После передачи в функцию данные никак не изменяются.
        :param defaults: Данные, которые вставляются по умолчанию БЕЗ ПРОВЕРКИ. Используется, например, чтобы
                         установить ссылку на ntreobq объект, создавая back_o2o или back_fk
        :param is_root: Явно указывает находимся ли мы в корне или функция create вызвана другим Repository.create
        :param run_in_transaction: По умолчанию равно параметру is_root.
                                   Указывает нужно ли помещать вызов функции в транзакцию. Если функция уже находится в
                                   транзации, то новый контекст транзакции сломает отлов ошибки и собъет connection.
        :param validate: По умолчанию равно параметру is_root.
                         Стоит вручную передавать False, если передаются валидированные данные. Автоматически False
                         передается вместе с is_root, когда Repository.create вызывается из другой функции.
        """
        self.raise_if_read_only_repository()

        validate = is_root if validate is None else validate
        run_in_transaction = is_root if run_in_transaction is None else run_in_transaction

        if validate:
            await self.validate(data, instance)
        # TODO: clean_edit_data for history

        async def get_updated_instance() -> MODEL:
            direct_related = {}
            sorted_data: SortedData = self.sort_data_by_field_types(data)

            for t in ('o2o', 'fk'):
                for field_name, value in getattr(sorted_data, t).items():
                    rel_instance = await self.get_relational(field_name, instance=instance)
                    remote_repository = self.repository_of(field_name)(
                        by=f'{self.by}__{self.model.__name__}',
                        extra=self.extra
                    )
                    if rel_instance:
                        await remote_repository.edit(rel_instance, value, is_root=False)
                    else:
                        direct_related[field_name] = await remote_repository.create(value, is_root=False)

            for t in ('o2o_pk', 'fk_pk'):
                for field_name, value in getattr(sorted_data, t).items():
                    direct_related[field_name] = value

            await self.handle_edit(
                instance=instance,
                data={**(defaults or {}), **sorted_data.db_field, **direct_related},
                extra_data=sorted_data.extra
            )

            for field_name, value in sorted_data.back_o2o.items():
                remote_repository = self.repository_of(field_name)(
                    by=f'{self.by}__{self.model.__name__}',
                    extra=self.extra
                )
                rel_instance = await self.get_relational(field_name, instance=instance)
                if rel_instance:
                    await remote_repository.edit(rel_instance, value, is_root=False)
                else:
                    relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                    await remote_repository.create(value, defaults={relation_field: instance.pk}, is_root=False)

            for field_name, bfk_data in sorted_data.back_fk.items():
                remote_repository = self.repository_of(field_name)(
                    by=f'{self.by}__{self.model.__name__}',
                    extra=self.extra
                )
                relation_field = self.get_field_instance(field_name).relation_source_field  # type: ignore
                rel_instances_map = await self.get_relational_list(field_name, in_map=True, instance=instance)

                for value in bfk_data:
                    if 'pk' in value:
                        rel_instance = rel_instances_map.pop(value['pk'])
                        await remote_repository.edit(
                            rel_instance,
                            {k: v for k, v in value.items() if k != 'pk'},
                            is_root=False
                        )
                    else:
                        await remote_repository.create(
                            value,
                            defaults={relation_field: instance.pk},
                            is_root=False
                        )
                if rel_instances_map:
                    await remote_repository.delete_many([v.pk for v in rel_instances_map.values()])

            await self.post_edit(instance)
            return instance

        if run_in_transaction:
            async with in_transaction():
                updated_instance = await get_updated_instance()
                return await self.get_one(updated_instance.pk)
        else:
            return await get_updated_instance()

    async def post_edit(self, instance: MODEL) -> None:
        """Override this function"""
        pass

    async def delete_many(self, item_pk_list: list[PK]) -> int:
        self.raise_if_read_only_repository()
        return await self._delete_many(item_pk_list)

    async def _delete_many(self, item_pk_list: list[PK]) -> int:
        raise NotImplementedError('Для этой модели не определено множественное удаление')

    async def delete_one(self, instance: MODEL) -> None:
        self.raise_if_read_only_repository()
        await self._delete_many(instance)

    async def _delete_one(self, instance: MODEL) -> None:
        raise NotImplementedError('Для этой модели не определено удаление')

    async def check_fk_exists(self, field_name: str, item_pk: PK) -> BaseModel:
        field_type, field = self.get_field_type_and_instance(field_name)

        if field_type in FieldTypes.no_pk_relation():
            related_field = cast(fields.relational.RelationalField, field)
        elif field_type in FieldTypes.pk_relation():
            related_field = cast(fields.relational.ForeignKeyFieldInstance, field.reference)
        else:
            raise Exception(f'{self.model}.{field_name} не относится к o2o, o2o_pk, fk, fk_pk, back_o2o, back_fk')
        related_instance = await related_field.related_model.get_or_none(pk=item_pk)
        if related_instance is None:
            raise NotFoundFK
        return related_instance

    async def check_unique(
            self,
            field_name: str,
            value: Any,
            data: DATA,
            instance: Optional[MODEL] = None,
    ) -> None:
        if instance and getattr(instance, field_name) == value:
            return
        if await self.model.exists(**{field_name: value}):
            raise NotUnique

    async def check_unique_together(
            self,
            data: DATA,
            instance: Optional[MODEL] = None
    ) -> None:
        """Недоделано"""
        raise NotImplementedError
        # errors = ObjectErrors()
        # for combo in self.opts().unique_together:
        #     values = {}
        # if instance:
        # for field_name in combo:
        # field = self.get_field_instance(field_name)
        # :) посмотри какие именно значения добавляются в unique_together, если пишешь туда o2o и fk
        # if await self.model.exists(**values):
        #     errors.add('__root__', NotUniqueTogether(combo))
        # if errors:
        #     raise errors

    @classmethod
    def sort_data_by_field_types(cls, data: DATA) -> SortedData:
        _all_fields: dict[str, FieldTypes] = cls.describe().all
        sorted_data = SortedData()

        for key, value in data.items():
            field_type = _all_fields.get(key)
            if field_type is None:
                if key in cls.extra_allowed:
                    sorted_data.extra[key] = value
                    continue
                raise UnexpectedDataKey(f'`{key}` не представлен в `{cls.model}`')
            if field_type == FieldTypes.HIDDEN:
                raise UnexpectedDataKey(f'`{key}` скрыт в `{cls.model}`')
            field_type_value = cast(str, field_type.value)
            if field_type_value in sorted_data.__dict__:
                getattr(sorted_data, field_type_value)[key] = value
            else:
                sorted_data.db_field[key] = value
        return sorted_data

    async def validate(self, data: DATA, instance: Optional[MODEL] = None) -> None:
        errors = ObjectErrors()

        required, pairs = self.required_and_pairs()
        required = required if instance is None else {}

        sorted_data = self.sort_data_by_field_types(data)

        for t in SortedData.__annotations__.keys():
            for name, value in getattr(sorted_data, t).items():
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
                except (FieldError, ObjectErrors) as e:
                    errors.add(name, e)

        for name, related in required.items():
            errors.add('__root__', RequiredMissed(name, related))
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
        validator = getattr(self, f'_validate_{field_name}', None)
        if validator:
            return validator(value, data, instance)
        return default_validator(field_name, value, data, instance)

    async def get_relational(self, field_name: str, instance: MODEL = None) -> Optional[BaseModel]:
        instance = instance or self.instance
        rel_instance = getattr(instance, field_name)
        if isinstance(rel_instance, QuerySet):
            await instance.fetch_related(field_name)
            rel_instance = getattr(instance, field_name)
        return rel_instance

    @overload
    async def get_relational_list(self, field_name: str, in_map: bool, instance: MODEL = None) -> dict[PK, BaseModel]:
        ...

    @overload
    async def get_relational_list(self, field_name: str, instance: MODEL = None) -> list[BaseModel]:
        ...

    async def get_relational_list(
            self,
            field_name: str,
            in_map: bool = False,
            instance: MODEL = None,
    ) -> list[BaseModel] | dict[PK, BaseModel]:
        instance = instance or self.instance
        rel_instances: list[BaseModel] = getattr(instance, field_name)
        if isinstance(rel_instances, QuerySet):
            await instance.fetch_related(field_name)
            rel_instances = getattr(instance, field_name)
        if in_map:
            return {i.pk: i for i in rel_instances}
        return rel_instances

    async def validate_relational(
            self,
            field_name: str,
            value: DATA,
            data: DATA,
            instance: Optional[MODEL]
    ):
        rel_instance = await self.get_relational(field_name, instance=instance) if instance else None
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
            value: PK,
            data: DATA,
            instance: Optional[MODEL]
    ) -> Optional[BaseModel]:
        field = self.get_field_instance(field_name)

        if value is None:
            if not field.null:
                raise FieldRequired
            return

        if not isinstance(value, field.field_type):  # передали неправильный тип pk
            raise InvalidType(
                f'o2o_pk `{self.model}.{field_name}` data must be int, not {type(value)} ({value})'
            )

        value: PK
        await self.check_unique(field_name, value, data, instance)
        return await self.check_fk_exists(field_name, value)

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
            value: PK,
            data: DATA,
            instance: Optional[MODEL]
    ) -> Optional[BaseModel]:
        field = self.get_field_instance(field_name)

        if value is None:
            if not field.null:
                raise FieldRequired
            return

        if not isinstance(value, field.field_type):  # передали правильный тип pk
            raise InvalidType(
                f'fk_pk `{self.model}.{field_name}` data must be {PK}, not {type(value)} ({value})'
            )
        value: PK
        return await self.check_fk_exists(field_name, value)

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
            value: BackFKData,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        values_list = value
        remote_repository = self.repository_of(field_name)(
            by=f'{self.by}__{self.model.__name__}',
            extra=self.extra
        )
        list_errors = ListFieldError()

        if not isinstance(values_list, list) and all(isinstance(v, dict) for v in values_list):
            raise InvalidType(
                f'back_fk `{self.model}.{field_name}` `data-add` must be list[dict], '
                f'not {type(values_list)} ({values_list})'
            )

        if instance is None:
            if any(['pk' in v for v in values_list]):
                raise ValueError(f'pk может быть передан только если объект изменяется, а не создается')
            rel_instance_map = {}
        else:
            rel_instance_map = await self.get_relational_list(field_name, in_map=True, instance=instance)

        for i, val in enumerate(values_list):
            if 'pk' in val:
                rel_instance = rel_instance_map.get(val['pk'])
                if rel_instance is None:
                    list_errors.append(i, ObjectErrors().add('__root__', NotFoundFK))
                    continue
                try:
                    await remote_repository.validate(
                        {k: v for k, v in val.items() if k != 'pk'},
                        instance=rel_instance
                    )
                except ObjectErrors as err:
                    list_errors.append(i, err)
            else:
                try:
                    await remote_repository.validate(val)
                except ObjectErrors as err:
                    list_errors.append(i, err)

        if list_errors:
            raise list_errors

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

    async def validate_extra(
            self,
            field_name: str,
            value: Any,
            data: DATA,
            instance: Optional[MODEL]
    ) -> None:
        pass

    @classmethod
    def describe(cls) -> RepositoryDescription:
        description = descriptions.get(cls)
        if description is None:

            description = RepositoryDescription()
            opts = cls.opts()

            def add_to_hidden(_name: str, _field: fields.Field):
                description.hidden[_name] = _field
                description.all[_name] = FieldTypes.HIDDEN

            for name in opts.o2o_fields:
                field = cast(models.OneToOneFieldInstance, opts.fields_map[name])
                if name in cls.hidden_fields:
                    add_to_hidden(name, field)
                else:
                    description.o2o[name] = field
                    description.all[name] = FieldTypes.O2O
                source_field = field.source_field
                if source_field in cls.hidden_fields:
                    add_to_hidden(name, field)
                else:
                    description.o2o_pk[source_field] = opts.fields_map[source_field]
                    description.all[source_field] = FieldTypes.O2O_PK

            for name in opts.fk_fields:
                field = cast(models.ForeignKeyFieldInstance, opts.fields_map[name])
                if name in cls.hidden_fields:
                    add_to_hidden(name, field)
                else:
                    description.fk[name] = field
                    description.all[name] = FieldTypes.FK
                source_field = field.source_field
                if source_field in cls.hidden_fields:
                    add_to_hidden(name, field)
                else:
                    description.fk_pk[source_field] = opts.fields_map[source_field]
                    description.all[source_field] = FieldTypes.FK_PK

            for name in opts.backward_o2o_fields:
                field = cast(fields.relational.BackwardOneToOneRelation, opts.fields_map[name])
                if name in cls.hidden_fields:
                    add_to_hidden(name, field)
                else:
                    description.back_o2o[name] = field
                    description.all[name] = FieldTypes.BACK_O2O

            for name in opts.backward_fk_fields:
                field = cast(fields.relational.BackwardFKRelation, opts.fields_map[name])
                if name in cls.hidden_fields:
                    add_to_hidden(name, field)
                description.back_fk[name] = field
                description.all[name] = FieldTypes.BACK_FK

            if opts.m2m_fields:
                raise Exception('M2M запрещены здравым смыслом')

            for name in opts.db_fields:
                # если не o2o_pk/fk_pk
                if name not in description.all:
                    field = opts.fields_map[name]
                    if name in cls.hidden_fields:
                        add_to_hidden(name, field)
                    else:
                        description.db_field[name] = field
                        description.all[name] = field_instance_to_type[field.__class__]

            descriptions[cls] = description
        return description

    @classmethod
    def get_field_type(cls, field_name: str) -> FieldTypes:
        return cls.describe().all[field_name]

    @classmethod
    def get_field_instance(cls, field_name: str) -> fields.Field:
        _, field_instance = cls.get_field_type_and_instance(field_name)
        return field_instance

    @classmethod
    def get_field_type_and_instance(cls, field_name: str) -> tuple[FieldTypes, fields.Field]:
        field_type = cls.get_field_type(field_name)
        field_type_value = cast(str, field_type.value)
        if field_type_value in RepositoryDescription.__annotations__:
            return field_type, getattr(cls.describe(), field_type_value)[field_name]
        return field_type, cls.describe().db_field[field_name]

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
            for name, field in describe.db_field.items():
                if cls.field_is_required(field):
                    required[name] = None
            for name, field in {**describe.o2o, **describe.fk}.items():
                if cls.field_is_required(field):
                    required[name] = field.source_field
                    pairs[name] = field.source_field
            for name, field in {**describe.o2o_pk, **describe.fk_pk}.items():
                if cls.field_is_required(field):
                    required[name] = field.reference.model_field_name
                    pairs[name] = field.reference.model_field_name
            setattr(cls, '__required_and_pairs', (required, pairs))
        required, pairs = getattr(cls, '__required_and_pairs')
        return {**required}, {**pairs}

    @classmethod
    def repository_of(cls, field_name: str) -> Type["Repository"]:
        field_type, field = cls.get_field_type_and_instance(field_name)
        if field_type in FieldTypes.no_pk_relation():
            reference = cast(fields.relational.RelationalField, field)
        elif field_type in FieldTypes.pk_relation():
            reference = cast(fields.relational.RelationalField, field.reference)
        else:
            raise ValueError(
                f'Поле {cls.model}.{field_name} с типом {cls.get_field_type(field_name)} не может иметь репозиторий'
            )
        related_model: BaseModel = reference.related_model
        repo_name = cls.related_repositories.get(field_name, '__default__')
        repo = related_model.REPOSITORIES.get(repo_name)
        if repo is None:
            raise ValueError(
                f'У поля {cls.model}.{field_name} ({related_model}) нет репозитория {repo_name}'
            )
        return repo

    @classmethod
    def get_repo_name(cls) -> str:
        return cls._REPOSITORY_NAME

    @classmethod
    def entity(cls):
        repo_name = cls.get_repo_name()
        if repo_name != '__default__':
            return f'{cls.opts().full_name}.{repo_name}'
        return cls.opts().full_name

    @classmethod
    def get_translation(cls, lang: str) -> BaseTranslation:
        return getattr(cls, f'_TRANSLATION_{lang.upper()}', getattr(cls, f'_TRANSLATION_DEFAULT'))

    @classmethod
    def get_field_name_for_value(cls, name: str) -> str:
        if name in cls.calculated:
            return name
        field_type = cls.get_field_type(name)
        if field_type in FieldTypes.pk_relation():
            field = cls.get_field_instance(name)
            name = field.reference.model_field_name
        return name

    @classmethod
    def get_instance_value(cls, instance: MODEL, name: str) -> str:
        field_name = cls.get_field_name_for_value(name)
        return getattr(instance, field_name, UndefinedValue)
