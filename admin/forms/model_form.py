from typing import Type, Any, Callable, Optional

from tortoise import fields
from core.orm import fields as orm_fields

from core.enums import FieldTypes
from core.repository import Repository
from admin.widgets import inputs
from .form import Form
from .schema import FormSchema, InputGroup


PRIMITIVE = tuple | list


class ModelForm(Form):
    repository: Type[Repository]
    LANG: str
    create: bool
    primitive: PRIMITIVE

    def __init__(
            self,
            repository: Type[Repository],
            *,
            lang: str = 'RU',
            primitive: PRIMITIVE = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.repository = repository
        self.LANG = lang
        self.primitive = primitive

    def get_form_schema(self) -> FormSchema:
        return self.schema or self._generate_form_schema()

    def _generate_form_schema(self) -> FormSchema:
        primitive = self.primitive or self._generate_primitive()

        schema = FormSchema()
        for item in primitive:
            schema.add_row(self._from_primitive_item(item))
        return schema

    def _from_primitive_item(self, item: Any) -> inputs.UserInput | InputGroup:
        if isinstance(item, str):
            field_name, extra = item, None
        elif (
                isinstance(item, tuple)
                and len(item) == 2
                and isinstance(item[0], str)
                and isinstance(item[1], dict)
        ):
            field_name, extra = item
        elif isinstance(item, dict):
            group_field = item.pop('fields')
            group = InputGroup(**item)
            for f in group_field:
                group.add_field(self._from_primitive_item(f))
            return group
        elif isinstance(item, (inputs.UserInput, InputGroup)):
            return item
        else:
            raise ValueError(f'{type(item)}({item}) не подходит ни под какой из типов:)')
        field_type, field = self.repository.get_field_type_and_instance(field_name)
        creator = self._input_schema_creators[field_type]
        return creator(field, extra)

    def _generate_primitive(self) -> PRIMITIVE:
        describe = self.repository.describe()
        primitive = []
        for name, field in describe.db_field.items():
            if not field.generated:
                primitive.append(name)
        # for name, field in describe.o2o.items():
        #     if field.required:
        #         primitive.append(name)
        # for name, field in describe.o2o_pk.items():
        #     if not field.required:
        #         primitive.append(name)
        # for name, field in describe.fk.items():
        #     if field.required:
        #         primitive.append(name)
        # for name, field in describe.fk_pk.items():
        #     if not field.required:
        #         primitive.append(name)
        return primitive

    @property
    def _input_schema_creators(
            self
    ) -> dict[FieldTypes, Callable[[fields.Field, Optional[dict[str, Any]]], inputs.UserInput]]:
        return {  # type: ignore
            FieldTypes.INT: self.int_input_creator,
            FieldTypes.FLOAT: self.float_input_creator,
            FieldTypes.STR: self.str_input_creator,
            FieldTypes.TEXT: self.text_input_creator,
            FieldTypes.BOOL: self.bool_input_creator,
            FieldTypes.ENUM: self.enum_input_creator,
            FieldTypes.DATE: self.date_input_creator,
            FieldTypes.DATETIME: self.datetime_input_creator,
            # FieldTypes.O2O: self.input_creator,
            # FieldTypes.O2O_PK: self.input_creator,
            # FieldTypes.FK: self.input_creator,
            # FieldTypes.FK_PK: self.input_creator,
            # FieldTypes.BACK_O2O: self.input_creator,
            # FieldTypes.BACK_FK: self.input_creator,
            # FieldTypes.M2M: self.input_creator,
        }

    def input_creator_base_kwargs(self, field: fields.Field) -> dict[str, Any]:
        return {
            'name': field.model_field_name,
            'label': self.repository.translate_field(field.model_field_name, lang=self.LANG),
            'validate_on_blur': True,
            'required': self.repository.field_is_required(field),
        }

    def int_input_creator(
            self,
            field: fields.IntField | fields.SmallIntField | fields.BigIntField,
            extra: dict[str, Any] = None
    ) -> inputs.IntInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_value'] = field.constraints['ge']
        kwargs['max_value'] = field.constraints['le']
        if extra:
            kwargs.update(extra)
        return inputs.IntInput(**kwargs)

    def float_input_creator(
            self,
            field: orm_fields.FloatField,
            extra: dict[str, Any] = None
    ) -> inputs.FloatInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_value'] = field.constraints['ge']
        kwargs['max_value'] = field.constraints['le']
        if extra:
            kwargs.update(extra)
        return inputs.FloatInput(**kwargs)

    def str_input_creator(
            self,
            field: orm_fields.CharField,
            extra: dict[str, Any] = None
    ) -> inputs.StrInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_length'] = field.constraints['min_length']
        kwargs['max_length'] = field.constraints['max_length']
        if extra:
            kwargs.update(extra)
        return inputs.StrInput(**kwargs)

    def text_input_creator(
            self,
            field: fields.TextField,
            extra: dict[str, Any] = None
    ) -> inputs.TextInput:
        kwargs = self.input_creator_base_kwargs(field)
        if extra:
            kwargs.update(extra)
        return inputs.TextInput(**kwargs)

    def bool_input_creator(
            self,
            field: fields.BooleanField,
            extra: dict[str, Any] = None
    ) -> inputs.Checkbox:
        kwargs = self.input_creator_base_kwargs(field)
        if extra:
            kwargs.update(extra)
        return inputs.Checkbox(**kwargs)

    def enum_input_creator(
            self,
            field: fields.data.CharEnumFieldInstance | fields.data.IntEnumFieldInstance,
            extra: dict[str, Any] = None
    ) -> inputs.EnumChoice:
        kwargs = self.input_creator_base_kwargs(field)
        if extra:
            kwargs.update(extra)
        return inputs.EnumChoice(**kwargs)

    def date_input_creator(
            self,
            field: fields.DateField,
            extra: dict[str, Any] = None
    ) -> inputs.DateInput:
        kwargs = self.input_creator_base_kwargs(field)
        if extra:
            kwargs.update(extra)
        return inputs.DateInput(**kwargs)

    def datetime_input_creator(
            self,
            field: fields.DatetimeField,
            extra: dict[str, Any] = None
    ) -> inputs.DatetimeInput:
        kwargs = self.input_creator_base_kwargs(field)
        if extra:
            kwargs.update(extra)
        return inputs.DatetimeInput(**kwargs)
