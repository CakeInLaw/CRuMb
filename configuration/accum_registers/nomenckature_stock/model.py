from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.accum_registers import AccumRegister, AccumRegisterResult


if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureStock", "NomenclatureStockResult"]


class NomenclatureStock(AccumRegister):
    nomenclature_id: int
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='stock_history', on_delete=fields.CASCADE
    )
    count: float = orm_fields.FloatField()

    class Meta:
        table = "accum_register__nomenclature_stock"


class NomenclatureStockResult(AccumRegisterResult):
    nomenclature_id: int
    nomenclature: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        'directories.Nomenclature', related_name='stock', on_delete=fields.CASCADE
    )
    count: float = orm_fields.FloatField()

    class Meta:
        table = "accum_register__nomenclature_stock__result"
