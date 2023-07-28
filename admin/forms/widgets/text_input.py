from dataclasses import dataclass

from . import StrInputWidget, StrInput


class TextInputWidget(StrInputWidget):

    def __init__(
            self,
            min_lines: int = None,
            max_lines: int = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.input.multiline = True
        self.input.shift_enter = True
        self.input.min_lines = min_lines
        self.input.max_lines = max_lines
        self.__finalize_init__()


@dataclass
class TextInput(StrInput[TextInputWidget]):
    min_lines: int = None
    max_lines: int = None
    width: int | float = 500
    height: int | float = None

    @property
    def widget_type(self):
        return TextInputWidget
