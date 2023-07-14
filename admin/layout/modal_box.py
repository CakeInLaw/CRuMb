from typing import TYPE_CHECKING

from flet import Card

from .payload import Box

if TYPE_CHECKING:
    from admin.layout import ContentBox, PayloadInfo


class ModalBox(Card, Box):
    def __init__(
            self,
            parent: "ContentBox",
            info: "PayloadInfo"
    ):
        super().__init__()
        self.parent = parent
        self.info = info
        self.app = self.parent.app
        self.resource = self.app.find_resource(info.entity)

    async def did_mount_async(self):
        await self.load_content()

    async def load_content(self):
        self.content = await self.resource.get_payload(
            box=self,
            method=self.info.method,
            **self.info.query,
        )
        await self.app.update_async()

    async def reload_content(self):
        await self.load_content()

    async def close(self):
        await self.parent.close_modal(self)

    async def add_modal(self, info: "PayloadInfo") -> "ModalBox":
        return await self.parent.add_modal(info=info)

    async def change_title(self, title: str):
        pass
