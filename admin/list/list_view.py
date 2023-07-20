from typing import TYPE_CHECKING

from flet import Container, Column, Row, ElevatedButton

from admin.layout import PayloadInfo
from .datagrid import Datagrid

if TYPE_CHECKING:
    from admin.resource import Resource
    from admin.layout import BOX


class ListView(Container):
    def __init__(
            self,
            resource: "Resource",
            box: "BOX"
    ):
        super().__init__()
        self.resource = resource
        self.app = self.resource.app
        self.box = box

        self.datagrid = Datagrid(
            box=self.box,
            resource=self.resource,
            columns=self.resource.datagrid_columns,
        )
        self.actions = Row([])
        if 'create' in self.resource.methods:
            self.actions.controls.append(ElevatedButton('Создать', on_click=self.open_create_form))
        self.content = Column([self.actions, self.datagrid])

    async def prepare(self):
        await self.datagrid.update_items()

    async def open_create_form(self, e):
        await self.app.open(info=PayloadInfo(entity=self.resource.entity(), method='create'))
