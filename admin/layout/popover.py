from typing import TYPE_CHECKING, Callable, Coroutine

from flet import GestureDetector, Control, Stack

if TYPE_CHECKING:
    from admin.layout import ContentBox


class Popover(GestureDetector):
    def __init__(
            self,
            box: "ContentBox",
            content: Control,
            on_close: Callable[[], Coroutine[..., ..., None]] = None,
    ):
        super().__init__(
            on_tap=self.close,
            top=0,
            left=0,
            right=0,
            bottom=0
        )
        self.content = Stack(controls=[content])
        self.box = box
        self.on_close = on_close

    async def close(self, e=None):
        if self.on_close:
            await self.on_close()
        await self.box.close_popover(self)
