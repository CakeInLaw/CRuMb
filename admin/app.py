from typing import TYPE_CHECKING, Type

from flet import (
    UserControl,
    Page,
    PopupMenuItem,
    Container,
    Row,
    Column
)
import flet as ft

from .content import Content
from .layout import Header, Sidebar

if TYPE_CHECKING:
    from .resource import Resource


class CRuMbAdmin(UserControl):
    def __init__(self, page: Page):
        super().__init__()

        self.expand = True  # чтобы вложенные элементы тоже расширялись

        self.page = page
        self.appbar_items = [
            PopupMenuItem(text="Login"),
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Settings")
        ]
        self.appbar = Header(page=self.page)
        self.sidebar = Sidebar(page=self.page)
        self.appbar.toggle_nav_rail_button.on_click = self.sidebar.toggle_sidebar
        self.content = Content(page=self.page)

        self.page.appbar = self.appbar

    def build(self):
        return Row(
            controls=[
                self.sidebar,
                Container(
                    content=Column(
                        controls=[self.content],
                        expand=True,
                    ),
                    expand=True,
                    bgcolor='current',
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        blur_style=ft.ShadowBlurStyle.OUTER,
                        color='#1C1B1F,0.2'
                    )
                ),
            ],
            spacing=0,
        )

    @classmethod
    def register_resource(cls, resource: Type["Resource"]) -> None:
        pass
