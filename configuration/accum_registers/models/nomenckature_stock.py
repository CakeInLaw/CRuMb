from datetime import datetime
from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.accum_registers import AccumRegister, AccumRegisterResult
from configuration.constants import DOCUMENT_REF_LEN


if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureStock", "NomenclatureStockResult"]


class NomenclatureStock(AccumRegister):
    id: int = fields.BigIntField(pk=True)
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='stock_history', on_delete=fields.CASCADE
    )
    document_ref: str = orm_fields.CharField(max_length=DOCUMENT_REF_LEN)
    count: float = orm_fields.FloatField()
    dt: datetime = fields.DatetimeField()
    commit: str = fields.TextField()

    class Meta:
        table = "accum_register__nomenclature_stock"


class NomenclatureStockResult(AccumRegisterResult):
    id: int = fields.IntField(pk=True)
    nomenclature: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        'directories.Nomenclature', related_name='stock', on_delete=fields.CASCADE
    )
    count: float = orm_fields.FloatField()
    dt: datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "accum_register__nomenclature_stock__result"
