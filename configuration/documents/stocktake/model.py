from typing import Union

from tortoise import fields
from core.orm import fields as orm_fields

from ..base_nomenclature_move_documents.model import MoveDocument, MoveDocumentValuesList


__all__ = ["Stocktake", "StocktakeValue"]


class Stocktake(MoveDocument):
    """Документ инвентаризации (ИН).
    Работает не через списания и оприходования, а сам по себе.
    Может иметь отрицательное количество в списке"""

    PREFIX: str = 'ИН'

    values_list: list["StocktakeValue"] | fields.BackwardFKRelation["StocktakeValue"]

    class Meta:
        table = "doc__stocktakes"


class StocktakeValue(MoveDocumentValuesList):
    count: float = orm_fields.FloatField()
    owner: Union["Stocktake", fields.ForeignKeyRelation["Stocktake"]] = fields.ForeignKeyField(
        'documents.Stocktake', related_name='values_list', on_delete=fields.CASCADE
    )

    class Meta:
        table = "doc__stocktakes__values"
