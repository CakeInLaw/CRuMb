from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValue

if TYPE_CHECKING:
    from configuration.documents.models import Sale


__all__ = ["CustomerReturn", "CustomerReturnValue"]


class CustomerReturn(MoveDocument):
    """Документ возврата продажи товаров (ВПР) от покупателя"""

    PREFIX: str = 'ВПТ'

    sale: Union["Sale", fields.ForeignKeyRelation["Sale"]] = fields.ForeignKeyField(
        'documents.Sale', related_name='returns', on_delete=fields.RESTRICT
    )

    values_list: list["CustomerReturnValue"] | fields.BackwardFKRelation["CustomerReturnValue"]

    class Meta:
        table = "doc__customer_returns"
        ordering = ('dt',)


class CustomerReturnValue(MoveDocumentValue):
    count: float = orm_fields.FloatField(min_value=0)
    price: float = orm_fields.FloatField(min_value=0)
    doc: Union["CustomerReturn", fields.ForeignKeyRelation["CustomerReturn"]] = fields.ForeignKeyField(
        'documents.CustomerReturn', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__customer_returns__values"
        ordering = 'ordering',
