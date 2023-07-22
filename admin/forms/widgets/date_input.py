from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class DateInputWidget(InputWidget[date]):
    min_date: Optional[date]
    max_date: Optional[date]
    date_fmt = '%d.%m.%Y'

    @property
    def final_value(self) -> Optional[date]:
        return self.to_date()

    def __init__(
            self,
            *,
            min_date: Optional[date] = None,
            max_date: Optional[date] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.keyboard_type = KeyboardType.DATETIME
        self.min_date = min_date
        self.max_date = max_date

    def to_date(self) -> Optional[date]:
        if self.value == '':
            return
        return datetime.strptime(self.value, self.date_fmt).date()

    def has_changed(self) -> bool:
        return self.to_date() == self.initial_value

    def _validate(self) -> None:
        empty = self.value == ''
        if self.required and empty:
            raise InputValidationError('Обязательное поле')
        if empty:
            return None
        try:
            date_v = self.to_date()
        except ValueError:
            raise InputValidationError(f'Формат даты ({self.date_fmt})')
        if self.min_date is not None and date_v < self.min_date:
            raise InputValidationError(f'Минимум {self.min_date.strftime(self.date_fmt)}')
        if self.max_date is not None and date_v > self.max_date:
            raise InputValidationError(f'Максимум {self.max_date.strftime(self.date_fmt)}')

    def set_value(self, value: Optional[date], initial: bool = False):
        assert value is None or isinstance(value, date)
        if value is None:
            self.value = ''
        else:
            self.value = value.strftime(self.date_fmt)


@dataclass
class DateInput(Input[DateInputWidget]):
    min_date: Optional[date] = None
    max_date: Optional[date] = None

    @property
    def widget_type(self):
        return DateInputWidget

    @property
    def default_initial(self) -> Optional[date]:
        if self.required:
            return date.today()
