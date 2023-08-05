from typing import TYPE_CHECKING

from tortoise import fields

from configuration.enums import NomenclatureTypes
from core.orm import fields as orm_fields

from core.entities.directories import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["NomenclatureCategory"]


class NomenclatureCategory(Directory):
    id: int = orm_fields.IntField(pk=True)
    name: str = orm_fields.CharField(max_length=50)
    type: NomenclatureTypes = orm_fields.CharEnumField(NomenclatureTypes)

    nomenclatures: list["Nomenclature"] | fields.BackwardFKRelation["Nomenclature"]

    class Meta:
        table = "dir__nomenclature_category"

    def __str__(self) -> str:
        return self.name
