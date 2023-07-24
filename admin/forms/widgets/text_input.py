from dataclasses import dataclass

from . import StrInputWidget, StrInput


class TextInputWidget(StrInputWidget):

    def __init__(
            self,
            min_lines: int = 3,
            max_lines: int = 3,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.input.multiline = True
        self.input.shift_enter = True
        self.text.min_lines = min_lines
        self.input.min_lines = min_lines
        self.text.max_lines = max_lines
        self.input.max_lines = max_lines
        self.__finalize_init__()


@dataclass
class TextInput(StrInput[TextInputWidget]):
    min_lines: int = 3
    max_lines: int = 10

    @property
    def widget_type(self):
        return TextInputWidget
