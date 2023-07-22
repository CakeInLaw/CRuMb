from dataclasses import dataclass
from typing import Optional

from flet import TextField, InputBorder

from .user_input import UserInputWidget, UserInput, T, _I


class InputWidget(UserInputWidget[T], TextField):

    def __init__(
            self,
            **kwargs
    ):
        TextField.__init__(
            self,
            text_size=14,
            dense=True,
            border=InputBorder.NONE,
            content_padding=0,
            on_blur=self.handle_value_change_and_update,
        )
        UserInputWidget.__init__(self, **kwargs)


@dataclass
class Input(UserInput[_I]):
    pass
