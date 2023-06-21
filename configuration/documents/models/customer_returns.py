from typing import TYPE_CHECKING, Union

from tortoise import fields
from tortoise.validators import MinValueValidator

from .nomenclature_move_documents import Document, DocumentValue

if TYPE_CHECKING:
    from configuration.documents.models import Sale


__all__ = ["CustomerReturn", "CustomerReturnValue"]


class CustomerReturn(Document):
    """Документ возврата продажи товаров (ВПР) от покупателя"""

    PREFIX: str = 'ВПТ'

    sale: Union["Sale", fields.ForeignKeyRelation["Sale"]] = fields.ForeignKeyField(
        'models.Sale', related_name='returns', on_delete=fields.RESTRICT
    )

    values_list: list["CustomerReturnValue"] | fields.BackwardFKRelation["CustomerReturnValue"]

    class Meta:
        table = "doc__customer_returns"
        ordering = ('dt',)


class CustomerReturnValue(DocumentValue):
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    price: float = fields.FloatField(validators=[MinValueValidator(0)])
    doc: Union["CustomerReturn", fields.ForeignKeyRelation["CustomerReturn"]] = fields.ForeignKeyField(
        'models.CustomerReturn', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__customer_returns__values"
        ordering = ('order',)
