from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from flet import KeyboardType
from tortoise import timezone

from core.admin.exceptions import InputValidationError
from .input import InputWidget, Input


class DatetimeInputWidget(InputWidget[datetime]):
    min_dt: Optional[datetime]
    max_dt: Optional[datetime]
    dt_fmt = '%d.%m.%Y %H:%M:%S'

    @property
    def final_value(self) -> Optional[datetime]:
        return self.to_datetime()

    def __init__(
            self,
            *,
            min_dt: Optional[datetime] = None,
            max_dt: Optional[datetime] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.keyboard_type = KeyboardType.DATETIME
        self.min_dt = min_dt
        self.max_dt = max_dt
        self.__finalize_init__()

    def to_datetime(self) -> Optional[datetime]:
        if self.value == '':
            return
        return timezone.make_aware(datetime.strptime(self.value, self.dt_fmt))

    def _validate(self) -> None:
        empty = self.value == ''
        if self.required and empty:
            raise InputValidationError('Обязательное поле')
        if empty:
            return None
        try:
            datetime_v = self.to_datetime()
        except ValueError:
            raise InputValidationError(f'Формат {self.dt_fmt}')
        if self.min_dt is not None and datetime_v < self.min_dt:
            raise InputValidationError(f'Минимум {self.min_dt.strftime(self.dt_fmt)}')
        if self.max_dt is not None and datetime_v > self.max_dt:
            raise InputValidationError(f'Максимум {self.max_dt.strftime(self.dt_fmt)}')

    def set_value(self, value: Optional[datetime], initial: bool = False) -> None:
        assert value is None or isinstance(value, datetime)
        if value is None:
            self.value = ''
        else:
            self.value = timezone.make_naive(value).strftime(self.dt_fmt)


@dataclass
class DatetimeInput(Input[DatetimeInputWidget]):
    min_dt: Optional[datetime] = None
    max_dt: Optional[datetime] = None

    @property
    def widget_type(self):
        return DatetimeInputWidget
