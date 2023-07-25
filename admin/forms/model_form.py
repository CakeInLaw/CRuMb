from typing import TYPE_CHECKING, Any, Callable, Optional, Type, Coroutine

from flet import ElevatedButton, Row

from core.exceptions import ObjectErrors
from core.enums import NotifyStatus

from admin.layout import PayloadInfo
from .widgets import UserInput, UndefinedValue
from . import Form, Primitive, FormSchema, WidgetSchemaCreator

if TYPE_CHECKING:
    from core.repository import Repository
    from admin.resource import Resource
    from admin.layout import BOX
    from core.orm import BaseModel


class ModelForm(Form):

    def __init__(
            self,
            resource: "Resource",
            box: "BOX",
            *,
            instance: Optional["BaseModel"] = None,
            primitive: Primitive = None,
            is_subform: bool = False,
            on_success: Callable[["ModelForm", "BaseModel"], Coroutine[Any, Any, None]] = None,
            on_error: Callable[["ModelForm", ObjectErrors], Coroutine[Any, Any, None]] = None,
            **kwargs
    ):
        super().__init__(app=resource.app, box=box, **kwargs)
        self.resource = resource
        self.instance = instance
        self.is_subform = is_subform
        self.primitive = primitive
        self.on_success = on_success or self.on_success_default
        self.on_error = on_error or self.on_error_default

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
        schema = FormSchema()
        widget_creator = WidgetSchemaCreator(resource=self.resource)
        for item in self.primitive:
            schema.add_item(widget_creator.from_primitive_item(item))
        return schema

    @staticmethod
    async def on_success_default(form: "ModelForm", instance: "BaseModel"):
        if form.create:
            await form.box.close()
            await form.app.open(PayloadInfo(
                entity=form.resource.entity(),
                method='edit',
                query={'pk': instance.pk}
            ))
        else:
            await form.box.reload_content()

    @staticmethod
    async def on_error_default(form: "ModelForm", error: ObjectErrors):
        pass

    async def on_click_create(self, e):
        if not self.form_is_valid():
            await self.update_async()
            return
        try:
            instance = await self.repository(
                by='admin',
                extra={'target': 'create'}
            ).create(self.cleaned_data())
            await self.app.notify('Создан 1 элемент', NotifyStatus.SUCCESS)
            await self.on_success(form=self, instance=instance)
        except ObjectErrors as err:
            self.set_object_errors(err)
            await self.update_async()
            await self.app.notify('Исправьте ошибки', NotifyStatus.ERROR)
            await self.on_error(form=self, error=err)

    def create_btn(self) -> ElevatedButton:
        return ElevatedButton('Создать', on_click=self.on_click_create)

    async def on_click_edit(self, e):
        if not self.form_is_valid():
            await self.update_async()
            return
        try:
            instance = await self.repository(
                by='admin',
                extra={'target': 'create'}
            ).edit(self.instance, self.cleaned_data())
            await self.app.notify('Элемент изменен', NotifyStatus.SUCCESS)
            await self.on_success(form=self, instance=instance)
        except ObjectErrors as err:
            self.set_object_errors(err)
            await self.update_async()
            await self.app.notify('Исправьте ошибки', NotifyStatus.ERROR)
            await self.on_error(form=self, error=err)

    def edit_btn(self) -> ElevatedButton:
        return ElevatedButton('Изменить', on_click=self.on_click_edit)

    def get_action_bar(self) -> Row:
        action_bar = super().get_action_bar()
        action_bar.controls.append(self.create_btn() if self.create else self.edit_btn())
        return action_bar
