from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.documents.model import Document, DocumentListValue

if TYPE_CHECKING:
    from configuration.directories.models import Employee, Nomenclature


__all__ = ["MoveDocument", "MoveDocumentValuesList"]


class MoveDocument(Document):
    """Базовая модель для всех документов движения"""

    responsible: Union["Employee", fields.ForeignKeyRelation["Employee"]] = fields.ForeignKeyField(
        'directories.Employee', on_delete=fields.RESTRICT
    )

    class Meta:
        abstract = True


class MoveDocumentValuesList(DocumentListValue):
    """Базовая модель списка для документов движения номенклатуры"""

    nomenclature_id: int
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', on_delete=fields.RESTRICT
    )
    count: float = orm_fields.FloatField(min_value=0)

    class Meta:
        abstract = True
