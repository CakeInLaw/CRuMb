from core.orm import fields as orm_fields

from core.entities.directories import Directory
from configuration.enums import OperationTypes


__all__ = ["OperationReason"]


class OperationReason(Directory):
    id: int = orm_fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=40)
    operation_type: OperationTypes = orm_fields.IntEnumField(OperationTypes)

    class Meta:
        table = "dir__operation_reasons"

    def __str__(self) -> str:
        return self.name
