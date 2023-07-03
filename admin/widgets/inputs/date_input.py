from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class DateInputWidget(InputWidget[date]):
    min_date: Optional[date]
    max_date: Optional[date]
    date_fmt = '%d.%m.%Y'

    def __init__(
            self,
            *,
            min_date: Optional[date] = None,
            max_date: Optional[date] = None,
            **kwargs
    ):
        kwargs['keyboard_type'] = KeyboardType.DATETIME
        super().__init__(**kwargs)
        self.min_date = min_date
        self.max_date = max_date

    def _validate(self, v: str) -> None:
        empty = v == ''
        if self.required and empty:
            raise InputValidationError('Обязательное поле')
        if empty:
            return None
        try:
            date_v = self.to_date(v)
        except ValueError:
            raise InputValidationError(f'Формат даты ({self.date_fmt})')
        if self.min_date is not None and date_v < self.min_date:
            raise InputValidationError(f'Минимум {self.min_date.strftime(self.date_fmt)}')
        if self.max_date is not None and date_v > self.max_date:
            raise InputValidationError(f'Максимум {self.max_date.strftime(self.date_fmt)}')

    @classmethod
    def to_date(cls, v) -> date:
        return datetime.strptime(v, cls.date_fmt).date()

    def to_value(self) -> Optional[date]:
        if self.value == '':
            return
        return self.to_date(self.value)

    def _set_initial_value(self, value: date) -> None:
        value = date.today() if value is None else value
        self.value = value.strftime(self.date_fmt)


@dataclass
class DateInput(Input[DateInputWidget]):
    min_date: Optional[date] = None
    max_date: Optional[date] = None

    @property
    def widget_type(self):
        return DateInputWidget
