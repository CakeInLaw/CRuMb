from typing import TYPE_CHECKING, Type, Optional, Callable, Coroutine, Any

from flet import Container, Column, Row, ElevatedButton

from core.orm import BaseModel
from .datagrid import Datagrid

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.resource import Resource


class ChoiceView(Container):
    def __init__(
            self,
            app: "CRuMbAdmin",
            resource: "Resource",
            current_chosen: Optional[BaseModel],
            handle_confirm: Callable[[Optional[BaseModel]], Coroutine[Any, Any, None]]
    ):
        super().__init__(expand=True)
        self.app = app
        self.resource = resource
        self.current_chosen = current_chosen
        self.handle_confirm = handle_confirm

        self.datagrid = Datagrid(
            app=self.app,
            repository=self.resource.repository,
            columns=self.resource.datagrid_columns,
        )
        self.actions = Row([ElevatedButton('Выбрать', on_click=self.make_choice)])
        self.content = Column([self.actions, self.datagrid], expand=True)

    async def make_choice(self, e):
        await self.handle_confirm(self.current_chosen)

    async def prepare(self):
        await self.datagrid.update_items()
