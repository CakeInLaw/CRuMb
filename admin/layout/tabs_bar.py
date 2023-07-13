from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional

from flet import DragTarget, DragTargetAcceptEvent, Draggable, \
    Container, Row, IconButton, Text, \
    ScrollMode, icons, border

from .loader import Loader

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.resource import Resource


@dataclass
class TabInfo:
    entity: str
    method: str
    query: dict[str, Any] = field(default_factory=dict)
    has_close: bool = True


class Tab(Draggable):
    def __init__(self, bar: "TabsBar", info: TabInfo):
        super().__init__(group='tab')

        self.bar = bar
        self.info = info

        self.text = Text(self.resource.name_plural)
        self.row = Row([self.text])
        if self.info.has_close:
            self.close_btn = IconButton(icon=icons.CLOSE_ROUNDED, on_click=self.handle_close)
            self.row.controls.append(self.close_btn)
        self.container = Container(
            border=border.symmetric(horizontal=border.BorderSide(1, 'black,0.2')),
            content=self.row
        )
        self.content = DragTarget(
            group='tab',
            content=self.container,
            on_accept=self.on_drag_accept
        )

        self.container.on_click = self.handle_click
        self.box = self.app.content_box.add_container()
        self.box.content = Loader()

    async def did_mount_async(self):
        self.box.content = content = await self.resource.methods[self.info.method](**self.info.query)
        if hasattr(content, '__tab_title__'):
            self.text.value = content.__tab_title__
        await self.app.update_async()

    @property
    def app(self) -> "CRuMbAdmin":
        return self.bar.app

    @property
    def resource(self) -> "Resource":
        if not hasattr(self, '_resource'):
            setattr(self, '_resource', self.app.find_resource(self.info.entity))
        return getattr(self, '_resource')

    @property
    def index(self):
        return self.bar.tab_index(self)

    async def handle_click(self, e):
        if self is not self.bar.selected:
            await self.bar.set_current_tab(self)

    async def handle_close(self, e):
        await self.bar.rm_tab(self)

    def before_remove(self):
        self.app.content_box.rm_container(self.box)

    def activate(self):
        self.box.visible = True
        self.container.bgcolor = 'black,0.2'

    def deactivate(self):
        self.box.visible = False
        self.container.bgcolor = 'white'

    async def on_drag_accept(self, e: DragTargetAcceptEvent):
        tab: Tab = self.page.get_control(e.src_id)
        await self.bar.move_tab(tab.index, self.index)


class TabsBar(Container):
    _selected: Optional[Tab] = None

    def __init__(self, app: "CRuMbAdmin"):
        super().__init__(bgcolor='white', border=border.only(bottom=border.BorderSide(1, 'black,0.5')))
        self.app = app
        self.tabs = []
        # строка в строке, потому что первая заполняет всё пространство, чтобы покрасилось в белый, а вторая скорллится
        self.content = Row([Row(
            controls=self.tabs,
            height=40,
            scroll=ScrollMode.ADAPTIVE,
            spacing=0,
        )])

    @property
    def selected(self) -> Optional[Tab]:
        return self._selected

    @selected.setter
    def selected(self, v: Optional[Tab]):
        assert v in self.tabs
        if self.selected is not None:
            self.selected.deactivate()
        self._selected = v
        if self.selected is not None:
            self.selected.activate()

    @property
    def selected_index(self) -> Optional[int]:
        if self.selected is None:
            return
        return self.tabs.index(self.selected)

    def tab_index(self, tab: Tab) -> int:
        return self.tabs.index(tab)

    def tab_by_info(self, info: TabInfo) -> Optional[Tab]:
        resource = self.app.find_resource(info.entity)
        for i, tab in enumerate(self.tabs):
            if (
                    tab.info.entity == info.entity
                    and tab.info.method == info.method
                    and resource.compare_tab(tab.info.method, tab.info.query, info.query)
            ):
                return tab
        return None

    async def set_current_tab(self, tab: Tab):
        self.selected = tab
        await self.app.update_async()

    async def rm_tab(self, tab: Tab):
        if tab is self.selected:
            self.selected = self.tabs[tab.index - 1]
        tab.before_remove()
        self.tabs.remove(tab)
        await self.app.update_async()

    async def create_tab(self, info: TabInfo):
        tab = Tab(bar=self, info=info)
        self.tabs.append(tab)
        await self.set_current_tab(tab)

    async def move_tab(self, idx_from: int, idx_to: int):
        if idx_from == idx_to:
            return
        tab = self.tabs.pop(idx_from)
        self.tabs.insert(idx_to, tab)
        await self.update_async()
