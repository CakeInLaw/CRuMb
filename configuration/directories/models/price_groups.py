from typing import TYPE_CHECKING

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from . import Customer
    from configuration.info_registers.models import NomenclaturePrice


__all__ = ["PriceGroup"]


class PriceGroup(Directory):
    id: int = orm_fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=50, unique=True)

    customers: list["Customer"] | fields.BackwardFKRelation["Customer"]
    prices: list["NomenclaturePrice"] | fields.BackwardFKRelation["NomenclaturePrice"]

    class Meta:
        table = "dir__price_groups"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name
