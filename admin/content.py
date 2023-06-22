
from flet import Page, UserControl, Container
import flet as ft


class Content(UserControl):
    root: Container

    def __init__(self, page: Page, **kwargs):
        kwargs.setdefault('expand', True)
        super().__init__(**kwargs)

        self.page = page
        self.root = Container(expand=True)
        self.sync_with_route(self.page.route)
        self.page.on_route_change = self.on_route_change

    def build(self):
        return self.root

    async def on_route_change(self, e: ft.RouteChangeEvent):
        self.sync_with_route(e.route)
        await self.root.update_async()

    def sync_with_route(self, route: str):
        self.root.content = ft.Text(route)
