from tortoise import fields


class DatetimeField(fields.DatetimeField):
    def __init__(self, editable: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.editable = False if self.auto_now else editable

    @property
    def constraints(self) -> dict:
        result = super().constraints
        result['editable'] = self.editable
        return result
