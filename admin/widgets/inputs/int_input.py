from dataclasses import dataclass
from typing import Optional

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class IntInputWidget(InputWidget[int]):
    min_value: Optional[int]
    max_value: Optional[int]

    def __init__(
            self,
            *,
            min_value: Optional[int] = None,
            max_value: Optional[int] = None,
            **kwargs
    ):
        kwargs['keyboard_type'] = KeyboardType.NUMBER
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, v: str) -> None:
        if self.required and v == '':
            raise InputValidationError('Обязательное поле')
        try:
            num = int(v)
        except ValueError:
            raise InputValidationError('Введите число')
        if self.min_value is not None and num < self.min_value:
            raise InputValidationError(f'Минимум {self.min_value}')
        if self.max_value is not None and num > self.max_value:
            raise InputValidationError(f'Максимум {self.max_value}')

    @property
    def final_value(self) -> int:
        return int(self.value)

    def _set_initial_value(self, value: int) -> None:
        self.value = '0' if value is None else str(value)


@dataclass
class IntInput(Input[IntInputWidget]):
    min_value: Optional[int] = None
    max_value: Optional[int] = None

    @property
    def widget_type(self):
        return IntInputWidget
