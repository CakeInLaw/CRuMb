from typing import TYPE_CHECKING

from flet import Page, UserControl, Container
import flet as ft

if TYPE_CHECKING:
    from .app import CRuMbAdmin


__all__ = ["Content"]


class Content(UserControl):
    app: "CRuMbAdmin"
    page: Page
    root: Container

    def __init__(self, app: "CRuMbAdmin", **kwargs):
        kwargs.setdefault('expand', True)
        super().__init__(**kwargs)

        self.app = app
        self.root = Container(
            expand=True,
            shadow=ft.BoxShadow(
                blur_radius=15,
                blur_style=ft.ShadowBlurStyle.OUTER,
                color='#1C1B1F,0.2'
            )
        )
        self.app.page.on_route_change = self.on_route_change

    async def did_mount_async(self):
        await self.sync_with_route(self.page.route)
        await self.root.update_async()

    def build(self):
        return self.root

    async def on_route_change(self, e: ft.RouteChangeEvent):
        await self.sync_with_route(e.route)
        await self.root.update_async()

    async def sync_with_route(self, route: str):
        print(route)
        resource = self.app.find_resource(route)
        if not resource:
            self.root.content = ft.Text('Не найдена нужная страница')
        else:
            self.root.content = await resource.datagrid()
