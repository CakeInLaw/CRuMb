from dataclasses import dataclass
from typing import Optional

from flet import Checkbox as FletCheckbox

from .user_input import UserInputWidget, UserInput
from ..widget_containers import BaseWidgetContainer, SimpleWidgetContainer


class CheckboxWidget(UserInputWidget[bool], FletCheckbox):

    def __init__(self, **kwargs):
        FletCheckbox.__init__(self)
        UserInputWidget.__init__(self, **kwargs)

        self.on_blur = self.end_change_event_handler
        self.__finalize_init__()

    def apply_container(self, container: BaseWidgetContainer):
        super().apply_container(container)
        if isinstance(self.container, SimpleWidgetContainer):
            self.container.with_label = False
            self.container.with_border = False
            self.label = self.label_text

    @property
    def final_value(self) -> Optional[bool]:
        return self.value

    def set_value(self, value: bool, initial: bool = False):
        assert isinstance(value, bool)
        self.value = value

    def set_error_text(self, text: Optional[str]):
        super().set_error_text(text)
        if isinstance(self.container, SimpleWidgetContainer):
            self.fill_color = 'error'

    def rm_error(self):
        super().rm_error()
        if isinstance(self.container, SimpleWidgetContainer):
            self.fill_color = None


@dataclass
class Checkbox(UserInput[CheckboxWidget]):

    @property
    def widget_type(self):
        return CheckboxWidget

    @property
    def default_initial(self) -> bool:
        return False
