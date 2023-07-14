from typing import TYPE_CHECKING

from flet import Control, Container, Stack, BoxShadow

from .loader import Loader
from .payload import Box
from .modal_box import ModalBox

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.layout import Tab, PayloadInfo

__all__ = ["ContentsBoxContainer", "ContentBox"]


class ContentBox(Container, Box):
    def __init__(
            self,
            box: "ContentsBoxContainer",
            tab: "Tab"
    ):
        super().__init__(padding=20)
        self.box = box
        self.tab = tab
        self.app = self.box.app
        self.resource = self.tab.resource
        self._stack_controls: list[Control] = [Loader()]
        self.content = Stack(self._stack_controls)

    @property
    def payload(self):
        return self._stack_controls[0]

    @payload.setter
    def payload(self, v: Control):
        self._stack_controls[0] = v

    async def did_mount_async(self):
        await self.load_content()

    async def load_content(self):
        self.payload = await self.resource.get_payload(
            box=self,
            method=self.tab.info.method,
            **self.tab.info.query,
        )
        if hasattr(self.payload, '__tab_title__'):
            self.tab.title = self.payload.__tab_title__
        await self.app.update_async()

    async def reload_content(self):
        await self.load_content()

    async def change_title(self, title: str):
        self.tab.title = title
        await self.tab.update_async()

    async def close(self):
        await self.tab.close()

    async def add_modal(self, info: "PayloadInfo") -> ModalBox:
        modal = ModalBox(parent=self, info=info)
        self._stack_controls.append(modal)
        await self.update_async()
        return modal

    async def close_modal(self, modal: ModalBox):
        if modal is self.payload or modal not in self._stack_controls:
            return
        self._stack_controls.remove(modal)
        await self.update_async()


class ContentsBoxContainer(Container):

    def __init__(self, app: "CRuMbAdmin"):
        super().__init__(
            expand=True,
            bgcolor='white',
            shadow=BoxShadow(
                blur_radius=15,
                offset=(0, 15),
                color='#1C1B1F,0.2'
            ),
        )
        self.app = app
        self.contents = []
        self.content = Stack(self.contents)

    def add_content_box(self, tab: "Tab") -> ContentBox:
        content_box = ContentBox(box=self, tab=tab)
        self.contents.append(content_box)
        return content_box

    def rm_content_box(self, content: ContentBox):
        self.contents.remove(content)
