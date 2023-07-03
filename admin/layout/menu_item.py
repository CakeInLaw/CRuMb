from typing import TYPE_CHECKING, Optional

from flet import Container, Row, Text, Icon

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from .menu_group import MenuGroup


class MenuItem(Container):

    def __init__(
            self,
            icon: str,
            label: str,
            destination: str,
            app: "CRuMbAdmin",
            parent: Optional["MenuGroup"] = None,
    ):
        super().__init__(
            on_click=self.go_link,
            border_radius=15,
            padding=10,
        )
        self.destination = destination
        self.app = app
        self.active = False
        self.parent = parent
        self.icon = Icon(icon, size=20)
        self.text = Text(label)
        self.content = Row([
            self.icon,
            self.text
        ])

    async def go_link(self, e):
        await self.app.page.go_async(self.destination)
        if self.app.sidebar.active is not self:
            await self.app.sidebar.set_active(self)

    def activate(self):
        self.bgcolor = 'red'
        if self.parent:
            self.parent.activate()

    def deactivate(self):
        self.bgcolor = None
        if self.parent:
            self.parent.deactivate()

    def minimize(self):
        self.text.visible = False

    def maximize(self):
        self.text.visible = True
