from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValuesList

if TYPE_CHECKING:
    from configuration.documents.models import Receive


__all__ = ["ProviderReturn", "ProviderReturnValue"]


class ProviderReturn(MoveDocument):
    """Документ возврата приобретения товаров (ВПТ) поставщику"""

    PREFIX: str = 'ВПТ'

    receive: Union["Receive", fields.ForeignKeyRelation["Receive"]] = fields.ForeignKeyField(
        'documents.Receive', related_name='returns', on_delete=fields.RESTRICT
    )

    values_list: list["ProviderReturnValue"] | fields.BackwardFKRelation["ProviderReturnValue"]

    class Meta:
        table = "doc__provider_returns"


class ProviderReturnValue(MoveDocumentValuesList):
    price: float = orm_fields.FloatField(min_value=0)
    owner: Union["ProviderReturn", fields.ForeignKeyRelation["ProviderReturn"]] = fields.ForeignKeyField(
        'documents.ProviderReturn', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__provider_returns__values"
