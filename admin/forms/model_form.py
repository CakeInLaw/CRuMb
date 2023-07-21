from typing import TYPE_CHECKING, Any, Callable, Optional, Type, Union

from flet import ElevatedButton, Row, Control, MainAxisAlignment
from tortoise import fields

from core.exceptions import ObjectErrors
from core.orm import BaseModel, fields as orm_fields
from core.enums import FieldTypes, NotifyStatus
from core.types import FK_TYPE

from admin.layout import PayloadInfo
from .inputs import UserInput, UndefinedValue
from . import Form, Primitive, inputs, FormSchema, InputGroup

if TYPE_CHECKING:
    from core.repository import Repository
    from admin.resource import Resource
    from admin.layout import BOX


class ModelForm(Form):

    def __init__(
            self,
            resource: "Resource",
            box: "BOX",
            *,
            instance: Optional[BaseModel] = None,
            primitive: Primitive = None,
            is_subform: bool = False,
            **kwargs
    ):
        super().__init__(app=resource.app, box=box, **kwargs)
        self.resource = resource
        self.instance = instance
        self.is_subform = is_subform
        self.primitive = primitive

    @property
    def repository(self) -> Type["Repository"]:
        return self.resource.repository

    @property
    def create(self) -> bool:
        return self.instance is None

    def initial_for(self, item: UserInput) -> Any:
        if self.create:
            return super().initial_for(item=item)
        else:
            field_name = self.repository.get_field_name_for_value(item.name)
            return getattr(self.instance, field_name, UndefinedValue)

    def get_form_schema(self) -> FormSchema:
        return self.schema or self._generate_form_schema()

    def _generate_form_schema(self) -> FormSchema:
        primitive = self.primitive or self._generate_primitive()

        schema = FormSchema()
        for item in primitive:
            schema.add_item(self._from_primitive_item(item))
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

    def _generate_primitive(self) -> Primitive:
        describe = self.repository.describe()
        primitive = Primitive()
        for name, field in describe.db_field.items():
            if not field.generated:
                primitive.add(name)
        if not self.is_subform:
            for name, field in describe.o2o.items():
                if field.required:
                    primitive.add(name)
            for name, field in describe.fk.items():
                if field.required:
                    primitive.add(name)
        for name, field in describe.o2o_pk.items():
            if self.is_subform or not field.required:
                primitive.add(name)
        for name, field in describe.fk_pk.items():
            if self.is_subform or not field.required:
                primitive.add(name)
        return primitive

    async def on_click_create(self, e):
        if not self.form_is_valid():
            return
        try:
            instance = await self.repository(
                by='admin',
                extra={'target': 'create'}
            ).create(self.cleaned_data())
            await self.app.notify('Создан 1 элемент', NotifyStatus.SUCCESS)
            await self.box.close()
            await self.app.open(PayloadInfo(
                entity=self.resource.entity(),
                method='edit',
                query={'pk': instance.pk}
            ))
        except ObjectErrors as err:
            self.set_object_errors(err)
            await self.update_async()
            await self.app.notify('Исправьте ошибки', NotifyStatus.ERROR)

    def create_btn(self) -> ElevatedButton:
        return ElevatedButton('Создать', on_click=self.on_click_create)

    async def on_click_edit(self, e):
        if not self.form_is_valid():
            return
        try:
            await self.repository(
                by='admin',
                extra={'target': 'create'}
            ).edit(self.instance, self.cleaned_data())
            await self.app.notify('Элемент изменен', NotifyStatus.SUCCESS)
            await self.box.reload_content()
        except ObjectErrors as err:
            self.set_object_errors(err)
            await self.update_async()
            await self.app.notify('Исправьте ошибки', NotifyStatus.ERROR)

    def edit_btn(self) -> ElevatedButton:
        return ElevatedButton('Изменить', on_click=self.on_click_edit)

    def get_action_bar(self) -> Control:
        return Row(
            controls=[self.create_btn() if self.create else self.edit_btn()],
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
            FieldTypes.O2O_PK: self.related_choice_creator,
            FieldTypes.FK: self.object_input_creator,
            FieldTypes.FK_PK: self.related_choice_creator,
            FieldTypes.BACK_O2O: self.related_choice_creator,
            FieldTypes.BACK_FK: self.objects_array_input_creator,
            # FieldTypes.M2M: self.input_creator,
        }

    def input_creator_base_kwargs(self, field: fields.Field) -> dict[str, Any]:
        return {
            'name': field.model_field_name,
            'label': self.resource.translate_field(field.model_field_name),
            'null': field.null,
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
        kwargs['empty_as_none'] = field.null
        kwargs.update(extra)
        return inputs.StrInput(**kwargs)

    def text_input_creator(
            self,
            field: fields.TextField,
            extra: dict[str, Any]
    ) -> inputs.TextInput:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['empty_as_none'] = field.null
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
            field: Union[
                fields.relational.ForeignKeyFieldInstance,
                fields.relational.OneToOneFieldInstance,
                fields.relational.BackwardFKRelation,
                fields.relational.BackwardOneToOneRelation,
            ],
            extra: dict[str, Any],
            data_row: bool = False
    ) -> inputs.ObjectInputBase:
        if data_row:
            object_input_class = inputs.ObjectInputTableRow
        else:
            object_input_class = inputs.ObjectInput
        kwargs = self.input_creator_base_kwargs(field)

        if 'fields' in extra:
            kwargs.update(extra)
            return object_input_class(**kwargs)

        primitive = None
        if 'primitive' in extra:
            primitive = extra.pop('primitive')
        relative_model_form = self.__class__(
            resource=self.resource.relative_resource(kwargs['name']),
            box=self.box,
            primitive=primitive,
            is_subform=True,
        )
        processed_fields: list[InputGroup, inputs.UserInput] = [
            relative_model_form._from_primitive_item(item)
            for item in relative_model_form.primitive or relative_model_form._generate_primitive()
        ]

        kwargs.update(extra)
        kwargs['fields'] = processed_fields
        return object_input_class(**kwargs)

    def related_choice_creator(
            self,
            field: FK_TYPE,
            extra: dict[str, Any]
    ) -> inputs.RelatedChoice:
        kwargs = self.input_creator_base_kwargs(field)
        kwargs['entity'] = self.resource.relative_resource(field.model_field_name).entity()
        kwargs.update(extra)
        return inputs.RelatedChoice(**kwargs)

    def objects_array_input_creator(
            self,
            field: fields.relational.BackwardFKRelation,
            extra: dict[str, Any]
    ) -> inputs.ObjectsArrayInput:
        kwargs = self.input_creator_base_kwargs(field)
        object_schema_info = extra.get('object_schema', {})
        if not isinstance(object_schema_info, inputs.ObjectInputTableRowWidget):
            extra['object_schema'] = self.object_input_creator(field, extra=object_schema_info, data_row=True)
        kwargs.update(extra)
        return inputs.ObjectsArrayInput(**kwargs)
