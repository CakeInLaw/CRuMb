from tortoise.fields import CharField as TortoiseCharField
from tortoise.validators import MinLengthValidator
from tortoise.exceptions import ConfigurationError


class CharField(TortoiseCharField):

    def __init__(self, min_length: int = None, **kwargs):
        self.min_length = min_length
        super().__init__(**kwargs)
        if self.min_length is not None:
            if min_length < 1:
                raise ConfigurationError("'min_length' must be >= 1")
            self.validators.append(MinLengthValidator(self.min_length))

    @property
    def constraints(self) -> dict:
        return {
            "min_length": self.min_length,
            "max_length": self.max_length,
        }
