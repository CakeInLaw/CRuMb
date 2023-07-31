import asyncio
import importlib
from typing import Type, TypeVar, Any, Callable, Coroutine

from flet import (
    Page, UserControl, Control, Column, Row, Text,
    SnackBar, ControlEvent,
    app as flet_app
)
from tortoise import Tortoise

from core.enums import NotifyStatus
from core.admin.layout import Header, TabsBar, PayloadInfo, Sidebar, MenuGroup, ContentsBoxContainer, Popover, Popup
from core.translations.app_translation import AppTranslation

from .resource import Resource


RESOURCE = TypeVar("RESOURCE", bound=Resource)


class CRuMbAdmin(UserControl):
    _resources: dict[str, Type["Resource"]] = {}
    BASE_URL = 'http://127.0.0.1'
    title: str = 'CRuMb Admin'
    menu_groups: list[Type[MenuGroup]] = []
    translations: AppTranslation

    def __init__(self, page: Page):
        super().__init__(expand=True)  # чтобы вложенные элементы тоже расширялись

        self.translation = self.translations.get('ru')
        self._init_resources()
        self.page = page

        self.appbar = Header(app=self)
        self.tabs_bar = TabsBar(app=self)
        self.sidebar = Sidebar(app=self)
        self.content_box_container = ContentsBoxContainer(app=self)

    def _init_resources(self) -> None:
        self._inited_resources = {entity: res(self) for entity, res in self._resources.items()}

    def build(self):
        return Column(
            controls=[
                self.appbar,
                self.tabs_bar,
                Row(
                    controls=[
                        self.sidebar,
                        self.content_box_container,
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
            if isinstance(group, tuple) and len(group) == 2:
                group, extra = group
                if not issubclass(group, MenuGroup) or not isinstance(extra, dict):
                    raise ValueError(f'Что-то не то передал: {group=}, {extra=}')
                method = extra.pop('method') if 'method' in extra else resource.default_method()
                query = extra.pop('query') if 'query' in extra else {}
                group.add_item_info(PayloadInfo(
                    entity=resource.entity(),
                    method=method,
                    query=query,
                    extra=extra,
                ))
            elif issubclass(group, MenuGroup):
                group.add_item_info(PayloadInfo(
                    entity=resource.entity(),
                    method=resource.default_method()
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
    def _init_translations(cls):
        cls.translations = importlib.import_module('configuration.translations').app_translations

    @classmethod
    def run_app(cls, **kwargs):
        kwargs.setdefault('target', cls.run_target)
        global APP
        cls._init_translations()
        APP = cls
        asyncio.get_event_loop().run_until_complete(cls.on_startup())
        importlib.import_module('configuration.repositories')
        importlib.import_module('configuration.resources')
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
        settings = importlib.import_module('configuration.settings')
        await Tortoise.init(config=settings.DATABASE)

    @classmethod
    async def on_shutdown(cls):
        await Tortoise.close_connections()

    async def open(self, info: PayloadInfo) -> None:
        if tab := self.tabs_bar.tab_by_info(info=info):
            await self.tabs_bar.set_current_tab(tab)
        else:
            await self.tabs_bar.create_tab(info=info)

    async def notify(
            self,
            content: Control | str,
            status: NotifyStatus = NotifyStatus.INFO,
            action: str = None,
            action_color: str = 'white',
            on_action: Callable[[ControlEvent], Coroutine[Any, Any, None] | None] = None
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
            show_close_icon=True,
            action=action,
            action_color=action_color,
            on_action=on_action
        ))

    async def dashboard(self):
        return Text('Тут будет дэшборд')

    async def add_popup(
            self,
            content: Control,
            title: str = None,
            on_close: Callable[[], Coroutine[..., ..., None]] = None,
    ) -> Popup:
        popup = Popup(
            app=self,
            content=content,
            title=title,
            on_close=on_close,
        )
        self.controls.append(popup)
        await self.update_async()
        return popup

    async def close_popup(self, popup: Popup) -> None:
        if popup not in self.controls:
            return
        self.controls.remove(popup)
        await self.update_async()

    async def add_popover(
            self,
            content: Control,
            on_close: Callable[[], Coroutine[..., ..., None]] = None,
    ) -> Popover:
        popover = Popover(
            app=self,
            content=content,
            on_close=on_close,
        )
        self.controls.append(popover)
        await self.update_async()
        return popover

    async def close_popover(self, popover: Popover) -> None:
        if popover not in self.controls:
            return
        self.controls.remove(popover)
        await self.update_async()


APP: Type[CRuMbAdmin] = None
