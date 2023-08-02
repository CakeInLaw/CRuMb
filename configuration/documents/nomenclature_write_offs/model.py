from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentListValue

if TYPE_CHECKING:
    from configuration.directories.models import Employee, OperationReason


__all__ = ["NomenclatureWriteOff", "NomenclatureWriteOffValue"]


class NomenclatureWriteOff(MoveDocument):
    """Документ списания номенклатуры (СП)"""

    PREFIX: str = 'СП'

    responsible_employee: Union["Employee", fields.ForeignKeyRelation["Employee"]] = fields.ForeignKeyField(
        'directories.Employee', related_name='nomenclature_write_offs_responsible_for', on_delete=fields.RESTRICT
    )
    reason: Union["OperationReason", fields.ForeignKeyRelation["OperationReason"]] = fields.ForeignKeyField(
        'directories.OperationReason', related_name='nomenclature_write_offs', on_delete=fields.RESTRICT
    )

    class Meta:
        table = "doc__nomenclature_write_offs"
        ordering = ("dt",)


class NomenclatureWriteOffValue(MoveDocumentListValue):
    count: float = orm_fields.FloatField(min_value=0)
    price: float = orm_fields.FloatField(min_value=0)
    doc: Union["NomenclatureWriteOff", fields.ForeignKeyRelation["NomenclatureWriteOff"]] = fields.ForeignKeyField(
        'documents.NomenclatureWriteOff', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__nomenclature_write_offs__values"
        ordering = ("order",)
