from typing import TYPE_CHECKING, Optional, Callable, Coroutine, Any

from flet import Container, Column, Row, ElevatedButton, DataRow

from core.orm import BaseModel
from .datagrid import Datagrid

if TYPE_CHECKING:
    from admin.resource import Resource
    from admin.layout import BOX


class ChoiceView(Container):
    def __init__(
            self,
            resource: "Resource",
            box: "BOX",
            current_chosen: Optional[BaseModel],
            handle_confirm: Callable[[Optional[BaseModel]], Coroutine[Any, Any, None]],
            handle_cancel: Callable[[], Coroutine[Any, Any, None]] = None,
    ):
        super().__init__()
        self.resource = resource
        self.app = self.resource.app
        self.box = box
        self.selected = current_chosen
        self.handle_confirm = handle_confirm
        self.handle_cancel = handle_cancel

        self.datagrid = Datagrid(
            box=self.box,
            resource=self.resource,
            columns=self.resource.datagrid_columns,
            on_active_change=self.on_active_change
        )
        self.actions = Row([
            ElevatedButton('Выбрать', on_click=self.on_choice),
            ElevatedButton('Очистить', on_click=self.on_clean),
            ElevatedButton('Отменить', on_click=self.on_cancel),

        ])
        self.content = Column([self.actions, self.datagrid], expand=True)

    async def prepare(self):
        await self.datagrid.update_items()

    async def close(self):
        await self.box.close()

    async def on_active_change(self, row: DataRow):
        self.selected = row.item

    async def on_clean(self, e):
        await self.handle_confirm(None)
        await self.close()

    async def on_choice(self, e):
        await self.handle_confirm(self.selected)
        await self.close()

    async def on_cancel(self, e):
        if self.handle_cancel:
            await self.handle_cancel()
        await self.close()
