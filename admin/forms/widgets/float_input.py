from dataclasses import dataclass
from typing import Optional

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class FloatInputWidget(InputWidget[float]):
    min_value: Optional[float | int]
    max_value: Optional[float | int]

    @property
    def final_value(self) -> float:
        return float(self.value)

    def __init__(
            self,
            *,
            min_value: Optional[float | int] = None,
            max_value: Optional[float | int] = None,
            decimal_places: int = 2,
            **kwargs
    ):
        kwargs['keyboard_type'] = KeyboardType.NUMBER
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places

    def _validate(self) -> None:
        empty = self.value == ''
        if self.required and empty:
            raise InputValidationError('Обязательное поле')
        if empty:
            return None
        try:
            num = float(self.value)
        except ValueError:
            raise InputValidationError('Введите число (с точкой)')
        if self.min_value is not None and num < self.min_value:
            raise InputValidationError(f'Минимум {self.min_value}')
        if self.max_value is not None and num > self.max_value:
            raise InputValidationError(f'Максимум {self.max_value}')

    def set_value(self, value: float, initial: bool = False):
        assert value is None or isinstance(value, float)
        self.value = '' if value is None else str(value)

    def _transform_value(self):
        value = self.value.replace(',', '.') if ',' in self.value else self.value
        try:
            self.value = f'{float(value):.{self.decimal_places}f}'
        except ValueError:
            pass


@dataclass
class FloatInput(Input[FloatInputWidget]):
    min_value: Optional[float | int] = None
    max_value: Optional[float | int] = None
    decimal_places: int = 2

    @property
    def widget_type(self):
        return FloatInputWidget

    @property
    def default_initial(self) -> Optional[float]:
        if self.required:
            return 0.0

    @property
    def is_numeric(self):
        return True
