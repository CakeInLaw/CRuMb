from typing import TYPE_CHECKING, TypeVar, Generic

from flet import Control

from .tooltip import WidgetTooltip

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
        self.widget = widget
        self.widget.container = self
        self.widget_tooltip = WidgetTooltip(self.widget, helper_text=self.widget.helper_text)

    def set_error_text(self, text: str):
        self.widget_tooltip.set_error_text(text)

    def rm_error(self):
        self.widget_tooltip.rm_error()
