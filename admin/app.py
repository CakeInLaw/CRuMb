import asyncio
from typing import Type, Optional, TypeVar

from flet import (
    UserControl,
    Page,
    PopupMenuItem,
    Row,
)
import flet as ft

from .content import Content
from .layout import Header, Sidebar

from .resource import Resource


RESOURCE = TypeVar("RESOURCE", bound="Resource")


class CRuMbAdmin(UserControl):
    _resources: dict[str, tuple[Type["Resource"], tuple[str | tuple[str, ...], ...]]] = {}
    _inited_resources: dict[str, "Resource"]
    LANG: str = "RU"
    title: str = 'CRuMb Admin'

    def __init__(self, page: Page):
        super().__init__(expand=True)  # чтобы вложенные элементы тоже расширялись

        self._init_resources()
        self.page = page
        self.appbar_items = [
            PopupMenuItem(text="Login"),
            PopupMenuItem(),  # divider
            PopupMenuItem(text="Settings")
        ]
        self.appbar = Header(app=self)
        self.sidebar = Sidebar(app=self)
        self.content = Content(app=self)

        self.page.appbar = self.appbar

    def build(self):
        return Row(
            controls=[
                self.sidebar,
                self.content,
            ],
            spacing=0,
        )

    @classmethod
    def register(
            cls,
            present_in: tuple[str | tuple[str, ...]] = (),
    ):
        def wrapper(resource: Type[RESOURCE]) -> Type[RESOURCE]:
            cls.register_resource(resource, present_in=present_in)
            return resource
        return wrapper

    @classmethod
    def register_resource(
            cls,
            resource: Type["Resource"],
            present_in: tuple[str | tuple[str, ...]] = (),
    ) -> None:
        route = resource.route()
        if route in cls._resources:
            raise ValueError(f'Ресурс с таким роутом уже существует ({route})')
        cls._resources[route] = resource, present_in

    def _init_resources(self) -> None:
        self._inited_resources = {route: res(self) for route, (res, _) in self._resources.items()}

    def find_resource(self, route: str) -> Optional["Resource"]:
        return self._inited_resources.get(route, None)

    def all_resources(self) -> dict[str, "Resource"]:
        return self._inited_resources

    @classmethod
    def run_app(cls, **kwargs):
        kwargs.setdefault('target', cls.run_target)
        asyncio.get_event_loop().run_until_complete(cls.on_startup())
        ft.app(**kwargs)
        asyncio.get_event_loop().run_until_complete(cls.on_shutdown())

    @classmethod
    async def run_target(cls, page: ft.Page):
        page.title = cls.title
        page.padding = 0
        app = cls(page)
        await page.add_async(app)

    @classmethod
    async def on_startup(cls):
        pass

    @classmethod
    async def on_shutdown(cls):
        pass
