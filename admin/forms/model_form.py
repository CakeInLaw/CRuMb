from typing import Type, Any, Callable

from flet import ElevatedButton, Row, Control, MainAxisAlignment
from tortoise import fields

from core.exceptions import ObjectErrors
from core.orm import fields as orm_fields

from core.enums import FieldTypes
from core.repository import Repository
from admin.widgets import inputs
from .form import Form
from .primitive import Primitive, PRIMITIVE
from .schema import FormSchema, InputGroup


class ModelForm(Form):

    def __init__(
            self,
            repository: Type[Repository],
            create: bool,
            *,
            lang: str = 'RU',
            primitive: PRIMITIVE = None,
            subform: bool = False,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.repository = repository
        self.create = create
        self.LANG = lang
        self.primitive = Primitive(primitive) if primitive else None
        self.subform = subform

    def get_form_schema(self) -> FormSchema:
        return self.schema or self._generate_form_schema()

    def _generate_form_schema(self) -> FormSchema:
        primitive = self.primitive or self._generate_primitive()

        schema = FormSchema()
        for item in primitive:
            schema.add_row(self._from_primitive_item(item))
        return schema

    def _from_primitive_item(self, item: Any) -> inputs.UserInput | InputGroup:
        if Primitive.is_schema(item):
            return item
        elif Primitive.is_group(item):
            group_field = item.pop('fields')
            group = InputGroup(**item)
            for f in group_field:
                group.add_field(self._from_primitive_item(f))
            return group
        elif Primitive.is_field_name(item):
            field_name, extra = item, {}
        elif Primitive.is_field_with_extra(item):
            field_name, extra = item
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
        if not self.subform:
            for name, field in describe.o2o.items():
                if field.required:
                    primitive.append(name)
            for name, field in describe.fk.items():
                if field.required:
                    primitive.append(name)
        # for name, field in describe.o2o_pk.items():
        #     if self.subform or not field.required:
        #         primitive.append(name)
        # for name, field in describe.fk_pk.items():
        #     if self.subform or not field.required:
        #         primitive.append(name)
        return primitive

    async def on_click_create(self, e):
        if not await self.form_is_valid():
            return
        try:
            await self.repository(
                by='admin',
                extra={'target': 'create'}
            ).create(self.cleaned_data())
        except ObjectErrors as err:
            await self.set_object_errors(err)

    def create_btn(self) -> ElevatedButton:
        return ElevatedButton('Создать', on_click=self.on_click_create)

    def get_submit_bar(self) -> Control:
        if self.create:
            return Row(
                controls=[self.create_btn()],
                alignment=MainAxisAlignment.END
            )

    @property
    def _input_schema_creators(
            self
    ) -> dict[FieldTypes, Callable[[fields.Field, dict[str, Any]], inputs.UserInput]]:
        return {  # type: ignore
            FieldTypes.INT: self.int_input_creator,
            FieldTypes.FLOAT: self.float_input_creator,
            FieldTypes.STR: self.str_input_creator,
            FieldTypes.TEXT: self.text_input_creator,
            FieldTypes.BOOL: self.bool_input_creator,
            FieldTypes.ENUM: self.enum_input_creator,
            FieldTypes.DATE: self.date_input_creator,
            FieldTypes.DATETIME: self.datetime_input_creator,
            FieldTypes.O2O: self.object_input_creator,
            # FieldTypes.O2O_PK: self.input_creator,
            FieldTypes.FK: self.object_input_creator,
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
            extra: dict[str, Any]
    ) -> inputs.IntInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_value'] = field.constraints['ge']
        kwargs['max_value'] = field.constraints['le']
        kwargs.update(extra)
        return inputs.IntInput(**kwargs)

    def float_input_creator(
            self,
            field: orm_fields.FloatField,
            extra: dict[str, Any]
    ) -> inputs.FloatInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_value'] = field.constraints['ge']
        kwargs['max_value'] = field.constraints['le']
        kwargs.update(extra)
        return inputs.FloatInput(**kwargs)

    def str_input_creator(
            self,
            field: orm_fields.CharField,
            extra: dict[str, Any]
    ) -> inputs.StrInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['min_length'] = field.constraints['min_length']
        kwargs['max_length'] = field.constraints['max_length']
        kwargs.update(extra)
        return inputs.StrInput(**kwargs)

    def text_input_creator(
            self,
            field: fields.TextField,
            extra: dict[str, Any]
    ) -> inputs.TextInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs.update(extra)
        return inputs.TextInput(**kwargs)

    def bool_input_creator(
            self,
            field: fields.BooleanField,
            extra: dict[str, Any]
    ) -> inputs.Checkbox:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs.update(extra)
        return inputs.Checkbox(**kwargs)

    def enum_input_creator(
            self,
            field: fields.data.CharEnumFieldInstance | fields.data.IntEnumFieldInstance,
            extra: dict[str, Any]
    ) -> inputs.EnumChoice:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs.update(extra)
        return inputs.EnumChoice(**kwargs)

    def date_input_creator(
            self,
            field: fields.DateField,
            extra: dict[str, Any]
    ) -> inputs.DateInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs.update(extra)
        return inputs.DateInput(**kwargs)

    def datetime_input_creator(
            self,
            field: fields.DatetimeField,
            extra: dict[str, Any]
    ) -> inputs.DatetimeInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs.update(extra)
        return inputs.DatetimeInput(**kwargs)

    def object_input_creator(
            self,
            field: fields.relational.ForeignKeyFieldInstance | fields.relational.OneToOneFieldInstance,
            extra: dict[str, Any]
    ) -> inputs.ObjectInput:
        kwargs = self.input_creator_base_kwargs(field)

        if 'fields' in extra:
            kwargs.update(extra)
            return inputs.ObjectInput(**kwargs)

        relative_model_form = self.__class__(
            repository=self.repository.repository_of(kwargs['name']),
            create=self.create,
            lang=self.LANG,
            subform=True,
        )
        if 'primitive' in extra:
            primitive = extra.pop('primitive')
        else:
            primitive = relative_model_form._generate_primitive()

        processed_fields: list[InputGroup, inputs.UserInput] = [
            relative_model_form._from_primitive_item(item)
            for item in primitive
        ]

        kwargs.update(extra)
        kwargs['fields'] = processed_fields
        return inputs.ObjectInput(**kwargs)
