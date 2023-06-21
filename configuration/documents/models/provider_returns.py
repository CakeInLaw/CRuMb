from typing import TYPE_CHECKING, Union

from tortoise import fields
from tortoise.validators import MinValueValidator

from .nomenclature_move_documents import Document, DocumentValue

if TYPE_CHECKING:
    from configuration.documents.models import Receive


__all__ = ["ProviderReturn", "ProviderReturnValue"]


class ProviderReturn(Document):
    """Документ возврата приобретения товаров (ВПТ) поставщику"""

    PREFIX: str = 'ВПТ'

    receive: Union["Receive", fields.ForeignKeyRelation["Receive"]] = fields.ForeignKeyField(
        'models.Receive', related_name='returns', on_delete=fields.RESTRICT
    )

    values_list: list["ProviderReturnValue"] | fields.BackwardFKRelation["ProviderReturnValue"]

    class Meta:
        table = "doc__provider_returns"
        ordering = ('dt',)


class ProviderReturnValue(DocumentValue):
    count: float = fields.FloatField(validators=[MinValueValidator(0)])
    price: float = fields.FloatField(validators=[MinValueValidator(0)])
    doc: Union["ProviderReturn", fields.ForeignKeyRelation["ProviderReturn"]] = fields.ForeignKeyField(
        'models.ProviderReturn', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__provider_returns__values"
        ordering = ('order', )
