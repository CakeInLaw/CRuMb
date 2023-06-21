from typing import TYPE_CHECKING, Union

from tortoise import fields
from tortoise.validators import MinValueValidator

from .nomenclature_move_documents import Document, DocumentValue

if TYPE_CHECKING:
    from configuration.directories.models import Customer
    from configuration.documents.models import CustomerReturn


__all__ = ["Sale", "SaleValue"]


class Sale(Document):
    """Документ продажи товаров (ПР)"""
    PREFIX: str = 'ПР'

    customer: Union["Customer", fields.ForeignKeyRelation["Customer"]] = fields.ForeignKeyField(
        'directories.Customer', related_name='sales', on_delete=fields.RESTRICT
    )

    values_list: list["SaleValue"] | fields.BackwardFKRelation["SaleValue"]
    returns: list["CustomerReturn"] | fields.BackwardFKRelation["CustomerReturn"]

    class Meta:
        table = 'doc__sales'
        ordering = ('dt',)


class SaleValue(DocumentValue):
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    price: float = fields.FloatField(validators=[MinValueValidator(0)])
    doc: Union["Sale", fields.ForeignKeyRelation["Sale"]] = fields.ForeignKeyField(
        'documents.Sale', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = 'doc__sales__values'
        ordering = ('order', )
