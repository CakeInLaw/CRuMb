import asyncio
from typing import Type, TypeVar

from flet import (
    Page, UserControl, Control, Row, Text, RouteChangeEvent,
    SnackBar, AlertDialog,
    app as flet_app
)

from core.enums import NotifyStatus
from .content import Content
from .layout import Header, Sidebar, MenuGroup

from .resource import Resource


RESOURCE = TypeVar("RESOURCE", bound="Resource")


class CRuMbAdmin(UserControl):
    _resources: dict[str, Type["Resource"]] = {}
    route_url_strategy: str = 'hash'
    BASE_URL = 'http://127.0.0.1'
    LANG: str = "RU"
    title: str = 'CRuMb Admin'
    menu_groups: list[Type[MenuGroup]] = []

    def __init__(self, page: Page):
        super().__init__(expand=True)  # чтобы вложенные элементы тоже расширялись

        self._init_resources()
        self.page = page
        self.page.on_route_change = self.on_route_change

        self.appbar = Header(app=self)
        self.sidebar = Sidebar(app=self)
        self.content = Content(app=self)

        self.page.appbar = self.appbar

    def _init_resources(self) -> None:
        self._inited_resources = {route: res(self) for route, res in self._resources.items()}

    def build(self):
        return Row(
            controls=[
                self.sidebar,
                self.content,
            ],
            spacing=0,
        )

    @classmethod
    def register(cls, resource: Type[RESOURCE]) -> Type[RESOURCE]:
        cls.register_resource(resource)
        return resource

    @classmethod
    def register_resource(cls, resource: Type["Resource"]) -> None:
        entity = resource.entity()
        if entity in cls._resources:
            raise ValueError(f'Ресурс с такой сущностью уже существует ({entity})')
        cls._resources[entity] = resource

    def find_resource(self, entity: str) -> "Resource":
        return self._inited_resources.get(entity)

    def all_resources(self) -> dict[str, "Resource"]:
        return self._inited_resources

    @classmethod
    def run_app(cls, **kwargs):
        kwargs.setdefault('target', cls.run_target)
        kwargs['route_url_strategy'] = cls.route_url_strategy
        asyncio.get_event_loop().run_until_complete(cls.on_startup())
        flet_app(**kwargs)
        asyncio.get_event_loop().run_until_complete(cls.on_shutdown())

    @classmethod
    async def run_target(cls, page: Page):
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

    @property
    def base_url(self) -> str:
        if self.route_url_strategy == 'hash':
            return self.BASE_URL + '/#'
        return self.BASE_URL

    def create_url(self, entity: str, method: str = '', **query) -> str:
        return self.base_url + self.create_path(entity, method, **query)

    def create_path(self, entity: str, method: str = '', **query):
        resource = self.find_resource(entity)
        assert method in resource.methods
        path = f'/{entity}{("/" + method) if method != "" else ""}'
        qs = '?' + '&'.join([f'{k}={v}' for k, v in query.items()]) if query else ''
        return path + qs

    async def did_mount_async(self):
        await self.sync_with_route()

    async def on_route_change(self, e: RouteChangeEvent):
        await self.sync_with_route()

    async def sync_with_route(self) -> None:
        q = self.page.query
        q()
        path = q.path[1:]
        query = q.to_dict
        if path == '':
            return
        if '/' in path:
            entity, method, *_ = path.split('/')
        else:
            entity, method = path, ''
        await self._open(entity, method, **query)

    async def _open(self, entity: str, method: str, **query) -> None:
        resource = self.find_resource(entity)
        self.content.content = await resource.methods.get(method, '')(**query)
        await self.update_async()

    async def open(self, entity: str, method: str, **query) -> None:
        self.page.route = self.create_path(entity, method, **query)
        await self.page.update_async()

    async def open_modal(self, entity: str, method: str, **query) -> None:
        resource = self.find_resource(entity)
        content = await resource.methods.get(method, '')(**query)
        await self.page.show_dialog_async(AlertDialog(
            modal=True,
            content=content,
            content_padding=10
        ))

    async def notify(
            self,
            content: Control | str,
            status: NotifyStatus = NotifyStatus.INFO
    ) -> None:
        if isinstance(content, str):
            content = Text(content)
        match status:
            case NotifyStatus.SUCCESS:
                bgcolor = 'primary'
            case NotifyStatus.ERROR:
                bgcolor = 'error'
            case NotifyStatus.WARN:
                bgcolor = 'orange'
            case _:
                bgcolor = None
        await self.page.show_snack_bar_async(SnackBar(
            content=content,
            bgcolor=bgcolor,
        ))
