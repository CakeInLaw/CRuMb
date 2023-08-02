from typing import TYPE_CHECKING, Union, Optional
from datetime import datetime

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.info_registers.model import InfoRegister, InfoRegisterResult
from configuration.constants import DOCUMENT_REF_LEN

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureCost", "NomenclatureCostResult"]


class NomenclatureCost(InfoRegister):
    id: int = orm_fields.BigIntField(pk=True)
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='cost_history', on_delete=fields.CASCADE
    )
    document_ref: Optional[str] = orm_fields.CharField(max_length=DOCUMENT_REF_LEN, null=True)
    cost: float = orm_fields.FloatField(min_value=0)
    count: float = orm_fields.FloatField(min_value=0)
    dt: datetime = orm_fields.DatetimeField()

    class Meta:
        table = "info_register__nomenclature_costs"
        ordering = ("dt", )


class NomenclatureCostResult(InfoRegisterResult):
    id: int = orm_fields.IntField(pk=True)
    nomenclature: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        'directories.Nomenclature', related_name='cost', on_delete=fields.CASCADE
    )
    cost: float = orm_fields.FloatField(min_value=0)
    dt: datetime = orm_fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "info_register__nomenclature_costs__result"
