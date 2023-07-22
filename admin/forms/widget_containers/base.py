from typing import TYPE_CHECKING, TypeVar, Generic

from flet import Control


if TYPE_CHECKING:
    from ..widgets import UserInputWidget
else:
    UserInputWidget = None


W = TypeVar('W', UserInputWidget, Control)


class BaseWidgetContainer(Generic[W]):
    def __init__(
            self,
            widget: W,
    ):
        super().__init__()
        self.widget = widget
