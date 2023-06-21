from typing import TYPE_CHECKING, Union

from tortoise import fields
from tortoise.validators import MinValueValidator

from .nomenclature_move_documents import Document, DocumentValue

if TYPE_CHECKING:
    from configuration.directories.models import Employee, OperationReason


__all__ = ["NomenclatureWriteOff", "NomenclatureWriteOffValue"]


class NomenclatureWriteOff(Document):
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


class NomenclatureWriteOffValue(DocumentValue):
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    price: float = fields.FloatField(validators=[MinValueValidator(0)])
    doc: Union["NomenclatureWriteOff", fields.ForeignKeyRelation["NomenclatureWriteOff"]] = fields.ForeignKeyField(
        'documents.NomenclatureWriteOff', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__nomenclature_write_offs__values"
        ordering = ("order",)
