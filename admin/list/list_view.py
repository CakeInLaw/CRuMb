from typing import TYPE_CHECKING, Type

from flet import Container, Column, Row, ElevatedButton

from .datagrid import Datagrid

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.resource import Resource


class ListView(Container):
    def __init__(
            self,
            app: "CRuMbAdmin",
            resource: "Resource",
    ):
        super().__init__(expand=True)
        self.app = app
        self.resource = resource

        self.datagrid = Datagrid(
            app=self.app,
            repository=self.resource.repository,
            columns=self.resource.datagrid_columns,
        )
        self.actions = Row([])
        if 'create' in self.resource.methods:
            self.actions.controls.append(ElevatedButton('Создать', on_click=self.open_create_form))
        self.content = Column([self.actions, self.datagrid], expand=True)

    async def prepare(self):
        await self.datagrid.update_items()

    async def open_create_form(self, e):
        await self.app.open(self.resource.entity(), 'create')
