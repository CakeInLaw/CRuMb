from dataclasses import dataclass
from typing import Optional, TypeVar

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class StrInputWidget(InputWidget[str]):
    _max_length: Optional[int]  # чтобы не работала встроенная штука с максимальной длиной, мб потом исправлю
    min_length: Optional[int]
    empty_as_none: bool

    def __init__(
            self,
            *,
            max_length: Optional[int] = None,
            min_length: Optional[int] = None,
            empty_as_none: bool = False,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._max_length = max_length
        self.min_length = min_length
        self.empty_as_none = empty_as_none
        assert not (self.empty_as_none and self.required), 'empty_as_none и required не могут быть одновременно True'

    @property
    def final_value(self) -> Optional[str]:
        if self.value == '' and self.empty_as_none:
            return None
        return self.value

    def _validate(self, v: str) -> None:
        if self._max_length is not None and len(v) > self._max_length:
            raise InputValidationError(msg=f'Максимум символов - {self._max_length}')
        if self.min_length is not None and len(v) < self.min_length:
            raise InputValidationError(msg=f'Минимум символов - {self.min_length}')

    def _set_initial_value(self, value: str) -> None:
        self.value = value or ''


S = TypeVar('S', bound=StrInputWidget)


@dataclass
class StrInput(Input[S]):
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    keyboard_type: Optional[KeyboardType] = None

    @property
    def widget_type(self):
        return StrInputWidget
