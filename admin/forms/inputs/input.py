from dataclasses import dataclass
from typing import Optional

from flet import TextField, InputBorder

from .user_input import UserInputWidget, UserInput, T, _I


class InputWidget(UserInputWidget[T], TextField):

    def __init__(
            self,
            **kwargs
    ):
        kwargs.setdefault('border', 2)
        kwargs.setdefault('border_radius', 12)
        kwargs.setdefault('text_size', 14)
        kwargs.setdefault('dense', True)
        super().__init__(**kwargs)
        self.on_blur = self.handle_value_change_and_update
        if self.in_table:
            self.apply_in_table_params()
        else:
            self.width = self.default_width

    def set_error_text(self, text: Optional[str]):
        self.error_text = text

    def apply_in_table_params(self):
        self.border = InputBorder.NONE
        self.content_padding = 0
        self.label = None


@dataclass
class Input(UserInput[_I]):
    pass
