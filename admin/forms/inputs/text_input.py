from dataclasses import dataclass

from . import StrInputWidget, StrInput


class TextInputWidget(StrInputWidget):

    def __init__(
            self,
            **kwargs
    ):
        kwargs['multiline'] = True
        kwargs['shift_enter'] = True
        super().__init__(**kwargs)


@dataclass
class TextInput(StrInput[TextInputWidget]):
    min_lines: int = 3

    @property
    def widget_type(self):
        return TextInputWidget
