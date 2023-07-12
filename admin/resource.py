from typing import TYPE_CHECKING, Generic, Type, Callable, Coroutine, Optional, Any, Union

from flet import Control, Text, icons

from core.types import PK
from core.orm.base_model import BaseModel
from core.exceptions import ItemNotFound
from core.repository import REPOSITORY
from admin.list import ListView, ChoiceView
from admin.forms import Form, ModelForm, Primitive

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin


__all__ = ["Resource"]


class Resource(Generic[REPOSITORY]):
    repository: Type[REPOSITORY]
    app: "CRuMbAdmin"
    ICON = icons.SPORTS_GYMNASTICS

    datagrid_columns: list[str]
    form_primitive: Primitive = None
    create_form_primitive: Primitive = None
    edit_form_primitive: Primitive = None

    def __init__(self, app: "CRuMbAdmin") -> None:
        self.app = app

    @property
    def name(self) -> str:
        return self.repository.translate_name(lang=self.app.LANG)

    @property
    def name_plural(self) -> str:
        return self.repository.translate_name_plural(lang=self.app.LANG)

    def translate_field(self, field_name: str) -> str:
        return self.repository.translate_field(field_name, lang=self.app.LANG)

    async def get_list_view(
            self,

    ) -> ListView:
        view = ListView(app=self.app, resource=self)
        await view.prepare()
        return view

    async def get_choice_view(
            self,
            current_chosen: Optional[BaseModel],
            handle_confirm: Callable[[Optional[BaseModel]], Coroutine[Any, Any, None]]
    ):
        view = ChoiceView(
            app=self.app,
            resource=self,
            current_chosen=current_chosen,
            handle_confirm=handle_confirm,
        )
        await view.prepare()
        return view

    def _get_form(self, *, obj: BaseModel = None, primitive: Primitive = None) -> Form:
        return ModelForm(
            app=self.app,
            repository=self.repository,
            lang=self.app.LANG,
            primitive=primitive,
            instance=obj
        )

    async def get_create_form(self) -> Control | Form:
        primitive = self.create_form_primitive or self.form_primitive
        return self._get_form(primitive=primitive)

    async def get_edit_form(self, pk: PK) -> Control | Form:
        try:
            obj = await self.repository(
                by='admin',
                extra={'target': 'edit'}
            ).get_one(pk)
        except ItemNotFound:
            return Text('Объект не найден')
        primitive = self.edit_form_primitive or self.form_primitive
        return self._get_form(obj=obj, primitive=primitive)

    async def delete(self):
        pass

    @classmethod
    def entity(cls) -> str:
        return cls.repository.entity()

    def _methods(self):
        return {
            '': self.get_list_view,
            'list': self.get_list_view,
            'choice': self.get_choice_view,
            'create': self.get_create_form,
            'edit': self.get_edit_form,
        }

    @property
    def methods(self) -> dict[str, Callable[[...], Coroutine]]:
        if not hasattr(self, '_cached_methods'):
            setattr(self, '_cached_methods', self._methods())
        return getattr(self, '_cached_methods')
