from typing import TYPE_CHECKING, Generic, Type

import flet as ft

from core.repository import REPOSITORY
from .datagrid import DatagridView
from .forms import Form, ModelForm

if TYPE_CHECKING:
    from .app import CRuMbAdmin


__all__ = ["Resource"]


class Resource(Generic[REPOSITORY]):
    repository: Type[REPOSITORY]
    app: "CRuMbAdmin"
    ICON = ft.icons.SPORTS_GYMNASTICS
    SELECTED_ICON = None
    datagrid_columns: list[str]

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

    def _get_form(self, *, create: bool = True) -> Form:
        return ModelForm(
            repository=self.repository,
            lang=self.app.LANG,
            create=create
        )

    def get_create_form(self):
        return self._get_form(create=True)

    def get_edit_form(self):
        return self._get_form(create=False)

    def delete(self):
        pass

    @classmethod
    def route(cls) -> str:
        return '/' + cls.repository.entity()

    # @classmethod
    # def routes(cls):
    #     return {
    #         '': cls.
    #     }
