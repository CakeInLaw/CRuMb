from typing import TYPE_CHECKING, Optional

from flet import ListTile, Text, Icon, ControlEvent

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from .menu_group import MenuGroup


class MenuItem(ListTile):

    def __init__(
            self,
            icon: str,
            label: str,
            entity: str,
            app: "CRuMbAdmin",
            parent: Optional["MenuGroup"] = None,
    ):
        super().__init__(
            dense=True,
            on_click=self.go_link,
            on_long_press=self.open_in_new_tab,
        )
        self.entity = entity
        self.app = app
        self.parent = parent
        self.leading = Icon(icon, size=24)
        self.title = Text(label, no_wrap=True, size=14)

    async def go_link(self, e: ControlEvent):
        await self.app.page.go_async(self.app.create_path(self.entity))
        if self.app.sidebar.active is not self:
            await self.app.sidebar.set_active(self)

    async def open_in_new_tab(self, e: ControlEvent):
        await self.app.page.launch_url_async(self.app.create_url(self.entity))

    def activate(self):
        self.selected = True
        if self.parent:
            self.parent.activate()

    def deactivate(self):
        self.selected = False
        if self.parent:
            self.parent.deactivate()

    def minimize(self):
        self.title.visible = False

    def maximize(self):
        self.title.visible = True
