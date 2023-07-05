from typing import TYPE_CHECKING

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory
from configuration.enums import Operations

if TYPE_CHECKING:
    from configuration.documents.models import NomenclatureWriteOff


__all__ = ["OperationReason"]


class OperationReason(Directory):
    id: int = fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=40)
    operation: Operations = fields.IntEnumField(Operations)

    nomenclature_write_offs: list["NomenclatureWriteOff"] | fields.ForeignKeyRelation["NomenclatureWriteOff"]

    class Meta:
        table = "dir__operation_reasons"
        ordering = ('id',)
