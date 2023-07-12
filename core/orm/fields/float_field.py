from typing import Optional

from tortoise.fields import FloatField as TortoiseFloatField
from tortoise.validators import MinValueValidator, MaxValueValidator


class FloatField(TortoiseFloatField):
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def __init__(
            self,
            min_value: float | int = None,
            max_value: float | int = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if min_value is not None:
            self.min_value = float(min_value)
            self.validators.append(MinValueValidator(self.min_value))
        if max_value is not None:
            self.max_value = float(max_value)
            self.validators.append(MaxValueValidator(self.max_value))

    @property
    def constraints(self) -> dict:
        return {
            'ge': self.min_value,
            'le': self.max_value,
        }
