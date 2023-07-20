from typing import Optional, Callable, Any, Coroutine

from flet import Control, OptionalNumber
from flet.canvas import Canvas, CanvasResizeEvent
from flet_core.canvas.shape import Shape


class SizeAwareContainer(Canvas):
    def __init__(
            self,
            shapes: Optional[list[Shape]] = None,
            content: Optional[Control] = None,
            resize_interval: OptionalNumber = None,
            on_resize: Callable[[CanvasResizeEvent], Coroutine[Any, Any, None] | None] = None,
            **kwargs
    ):
        super().__init__(
            shapes=shapes,
            content=content,
            resize_interval=resize_interval,
            on_resize=on_resize,
            **kwargs
        )
        self.current_width = 0
        self.current_height = 0
        self.on_resize = self.test

    def test(self, e: CanvasResizeEvent):
        self.current_width = e.width
        self.current_height = e.height
        print(self.current_width, self.current_height)
