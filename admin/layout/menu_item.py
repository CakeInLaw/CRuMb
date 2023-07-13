from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Any

from flet import ListTile, Text, Icon, ControlEvent


if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from .menu_group import MenuGroup


@dataclass
class MenuItemInfo:
    entity: str
    method: str = ''
    query: dict[str, Any] = field(default_factory=dict)


class MenuItem(ListTile):

    def __init__(
            self,
            icon: str,
            label: str,
            app: "CRuMbAdmin",
            entity: str,
            method: str,
            query: dict[str, Any] = None,
            parent: Optional["MenuGroup"] = None,
    ):
        super().__init__(
            dense=True,
            on_click=self.handle_click,
        )
        self.app = app
        self.parent = parent
        self.entity = entity
        self.method = method
        self.query = query or {}
        self.leading = Icon(icon, size=24)
        self.title = Text(label, no_wrap=True, size=14)

    async def handle_click(self, e: ControlEvent):
        await self.app.open(self.entity, self.method, **self.query)

    def minimize(self):
        self.title.visible = False

    def maximize(self):
        self.title.visible = True
