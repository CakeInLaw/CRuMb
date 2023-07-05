from typing import TYPE_CHECKING, Generic, Type, Callable, Coroutine

from flet import Control, Text, icons

from admin.forms.model_form import model_form_factory
from core.exceptions import ItemNotFound
from core.repository import REPOSITORY
from admin.datagrid import DatagridView
from admin.forms import Form
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
    datagrid_columns: list[str]
    present_in: tuple["MenuGroup"] = ()
    create_form = None
    edit_form = None

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

    def _get_form(self, *, create: bool) -> Type[Form]:
        return model_form_factory(self.repository)

    async def get_create_form(self) -> Control:
        form = self.create_form or self._get_form(create=True)
        return form()

    async def get_edit_form(self, pk: PK) -> Control:
        form = self.edit_form or self._get_form(create=False)
        try:
            obj = await self.repository(
                by='admin',
                extra={'target': 'edit'}
            ).get_one(pk)
        except ItemNotFound:
            return Text('Объект не найден')
        return form(initial_data=obj)

    async def delete(self):
        pass

    @classmethod
    def entity(cls) -> str:
        return cls.repository.entity()

    @property
    def methods(self) -> dict[str, Callable[[...], Coroutine]]:
        return {
            '': self.datagrid,
            'list': self.datagrid,
            'create': self.get_create_form,
            'edit': self.get_edit_form,
        }
