from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from flet import KeyboardType

from admin.exceptions import InputValidationError
from .input import InputWidget, Input


class DatetimeInputWidget(InputWidget[datetime]):
    min_dt: Optional[datetime]
    max_dt: Optional[datetime]
    dt_fmt = '%d.%m.%Y %H:%M:%S'

    def __init__(
            self,
            *,
            min_dt: Optional[datetime] = None,
            max_dt: Optional[datetime] = None,
            **kwargs
    ):
        kwargs['keyboard_type'] = KeyboardType.DATETIME
        super().__init__(**kwargs)
        self.min_dt = min_dt
        self.max_dt = max_dt

    def _validate(self, v: str) -> None:
        empty = v == ''
        if self.required and empty:
            raise InputValidationError('Обязательное поле')
        if empty:
            return None
        try:
            datetime_v = self.to_datetime(v)
        except ValueError:
            raise InputValidationError(f'Формат {self.dt_fmt}')
        if self.min_dt is not None and datetime_v < self.min_dt:
            raise InputValidationError(f'Минимум {self.min_dt.strftime(self.dt_fmt)}')
        if self.max_dt is not None and datetime_v > self.max_dt:
            raise InputValidationError(f'Максимум {self.max_dt.strftime(self.dt_fmt)}')

    @classmethod
    def to_datetime(cls, v) -> datetime:
        return datetime.strptime(v, cls.dt_fmt)

    def to_value(self) -> Optional[datetime]:
        if self.value == '':
            return
        return self.to_datetime(self.value)

    def _set_initial_value(self, value: datetime) -> None:
        value = datetime.now() if value is None else value
        self.value = value.strftime(self.dt_fmt)


@dataclass
class DatetimeInput(Input[DatetimeInputWidget]):
    min_dt: Optional[datetime] = None
    max_dt: Optional[datetime] = None

    @property
    def widget_type(self):
        return DatetimeInputWidget
