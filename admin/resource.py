from typing import TYPE_CHECKING, Generic, Type, Callable, Coroutine

from flet import Control, Text, icons

from admin.forms.model_form import PRIMITIVE
from core.orm.base_model import BaseModel
from core.exceptions import ItemNotFound
from core.repository import REPOSITORY
from admin.datagrid import DatagridView
from admin.forms import Form, ModelForm
from core.types import PK

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.layout import MenuGroup


__all__ = ["Resource"]


class Resource(Generic[REPOSITORY]):
    repository: Type[REPOSITORY]
    app: "CRuMbAdmin"
    ICON = icons.SPORTS_GYMNASTICS
    SELECTED_ICON = None
    present_in: tuple["MenuGroup"] = ()

    datagrid_columns: list[str]
    form_primitive = None
    create_form_primitive = None
    edit_form_primitive = None

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

    async def datagrid(self) -> DatagridView:
        dg = DatagridView(
            app=self.app,
            repository=self.repository,
            columns=self.datagrid_columns,
            pagination_per_page=1,
        )
        await dg.update_items()
        dg.pagination.rebuild()
        return dg

    def _get_form(self, *, obj: BaseModel = None, primitive: PRIMITIVE = None) -> Form:
        return ModelForm(
            self.repository,
            create=obj is None,
            lang=self.app.LANG,
            primitive=primitive,
            initial_data=obj
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
            '': self.datagrid,
            'list': self.datagrid,
            'create': self.get_create_form,
            'edit': self.get_edit_form,
        }

    @property
    def methods(self) -> dict[str, Callable[[...], Coroutine]]:
        if not hasattr(self, '_cached_methods'):
            setattr(self, '_cached_methods', self._methods())
        return getattr(self, '_cached_methods')
