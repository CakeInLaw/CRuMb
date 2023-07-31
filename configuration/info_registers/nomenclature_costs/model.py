from typing import TYPE_CHECKING, Union, Optional
from datetime import datetime

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.info_registers.model import InfoRegister
from configuration.constants import DOCUMENT_REF_LEN

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureCost"]


class NomenclatureCost(InfoRegister):
    id: int = orm_fields.BigIntField(pk=True)
    nomenclature: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='cost', on_delete=fields.RESTRICT
    )
    document_ref: Optional[str] = orm_fields.CharField(max_length=DOCUMENT_REF_LEN, null=True)
    cost: float = orm_fields.FloatField(min_value=0)
    count: float = orm_fields.FloatField(min_value=0)
    dt: datetime = fields.DatetimeField()

    class Meta:
        table = "info_register__nomenclature_costs"
        ordering = ("dt", )
