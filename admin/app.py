import asyncio
from typing import Type, TypeVar, Any

from flet import (
    Page, UserControl, Control, Column, Row, Text,
    SnackBar, AlertDialog,
    app as flet_app
)

from core.enums import NotifyStatus
from admin.layout.contentbox import ContentBox
from .layout import Header, TabsBar, TabInfo, Sidebar, MenuGroup, MenuItemInfo

from .resource import Resource


RESOURCE = TypeVar("RESOURCE", bound=Resource)


class CRuMbAdmin(UserControl):
    _resources: dict[str, Type["Resource"]] = {}
    BASE_URL = 'http://127.0.0.1'
    LANG: str = "RU"
    title: str = 'CRuMb Admin'
    menu_groups: list[Type[MenuGroup]] = []

    def __init__(self, page: Page):
        super().__init__(expand=True)  # чтобы вложенные элементы тоже расширялись

        self._init_resources()
        self.page = page

        self.appbar = Header(app=self)
        self.tabs_bar = TabsBar(app=self)
        self.sidebar = Sidebar(app=self)
        self.content_box = ContentBox(app=self)

        self.page.appbar = self.appbar

    def _init_resources(self) -> None:
        self._inited_resources = {entity: res(self) for entity, res in self._resources.items()}

    def build(self):
        return Column(
            controls=[
                self.tabs_bar,
                Row(
                    controls=[
                        self.sidebar,
                        self.content_box,
                    ],
                    spacing=0,
                    expand=True
                )
            ],
            spacing=0,
        )

    @classmethod
    def register(
            cls,
            present_in: tuple[Type["MenuGroup"] | tuple[Type["MenuGroup"], dict[str, Any]], ...] = ()
    ):
        def wrapper(resource: Type[RESOURCE]) -> Type[RESOURCE]:
            cls.register_resource(resource, present_in=present_in)
            return resource
        return wrapper

    @classmethod
    def register_resource(
            cls,
            resource: Type["Resource"],
            present_in: tuple[Type["MenuGroup"] | tuple[Type["MenuGroup"], dict[str, Any]], ...] = ()
    ) -> None:
        for group in present_in:
            if issubclass(group, MenuGroup):
                group.add_item_info(MenuItemInfo(
                    entity=resource.entity(),
                    method=resource.default_method()
                ))
            elif isinstance(group, tuple) and len(group) == 2:
                group, extra = group
                if not issubclass(group, MenuGroup) or not isinstance(extra, dict):
                    raise ValueError(f'Что-то не то передал: {group=}, {extra=}')
                group.add_item_info(MenuItemInfo(
                    entity=resource.entity(),
                    **extra
                ))
            else:
                raise TypeError(f'Что-то не то передал: {type(group)}, ({group})')

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

    async def open(self, entity: str, method: str, **query) -> None:
        tab_info = TabInfo(
            entity=entity,
            method=method,
            query=query
        )
        if tab := self.tabs_bar.tab_by_info(info=tab_info):
            await self.tabs_bar.set_current_tab(tab)
        else:
            await self.tabs_bar.create_tab(info=tab_info)

    async def open_modal(self, entity: str, method: str, **query) -> None:
        resource = self.find_resource(entity)
        content = await resource.methods[method](**query)
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

    async def dashboard(self):
        return Text('Тут будет дэшборд')
