from dataclasses import dataclass

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
            on_focus=self.start_change_event_handler,
            on_blur=self.end_change_event_handler,
        )
        UserInputWidget.__init__(self, **kwargs)


@dataclass
class Input(UserInput[_I]):
    pass
