from typing import TYPE_CHECKING, Optional

from flet import Container, Column
import flet as ft

from .btn_pin import BtnPin
from .menu_item import MenuItem

if TYPE_CHECKING:
    from ..app import CRuMbAdmin


__all__ = ["Sidebar"]


class Sidebar(Container):
    items: list[MenuItem]
    app: "CRuMbAdmin"

    active: Optional[MenuItem]

    def __init__(self, app: "CRuMbAdmin"):

        super().__init__(
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            animate=100,
        )
        self.app = app
        self.items = [
            MenuItem(
                icon=resource.ICON,
                label=resource.name_plural,
                destination=path,
                app=self.app
            )
            for path, resource in self.app.all_resources().items()
        ]
        self.active = None
        self.btn_pin = BtnPin(pinned=False, sidebar=self)
        self.content = Column([
            Container(
                content=Container(Column(self.items, scroll=ft.ScrollMode.ADAPTIVE, expand=True), padding=4),
                on_hover=self.toggle_size,
                expand=True
            ),
            self.btn_pin
        ])
        self.expanded = False

    async def did_mount_async(self):
        await self.set_suitable_active()

    async def toggle_size(self, e: ft.ControlEvent):
        if not self.btn_pin.pinned:
            self.expanded = e.data == 'true'
            await self.update_async()

    def minimize(self):
        self.width = 50
        for item in self.items:
            item.minimize()
        self.btn_pin.minimize()

    def maximize(self):
        self.width = 200
        for item in self.items:
            item.maximize()
        self.btn_pin.maximize()

    @property
    def expanded(self) -> bool:
        return self._expanded

    @expanded.setter
    def expanded(self, v: bool):
        if hasattr(self, '_expanded') and v == self.expanded:
            return
        self._expanded = v
        self.maximize() if self.expanded else self.minimize()

    async def set_active(self, item: Optional[MenuItem]):
        if self.active:
            self.active.deactivate()
        self.active = item
        if self.active:
            self.active.activate()
        await self.update_async()

    async def set_suitable_active(self):
        route: str = self.app.page.route
        if not route.startswith('/'):
            route = '/' + route
        if route.count('/') == 1:
            find = route
        else:
            find = route[:route.find('/', 1)]
        suitable_items = list(filter(lambda x: x.destination == find, self.items))
        await self.set_active(suitable_items[0] if suitable_items else None)
