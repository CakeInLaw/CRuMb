from typing import TYPE_CHECKING, Union, Optional

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory
from configuration.enums import NomenclatureTypes, NomenclatureUnits

if TYPE_CHECKING:
    from configuration.directories.models import RecipeCard, NomenclatureCategory
    from configuration.accum_registers.models import NomenclatureStockResult
    from configuration.info_registers.models import NomenclatureCostResult


__all__ = ["Nomenclature"]


class Nomenclature(Directory):
    id: int = orm_fields.BigIntField(pk=True)

    name: str = orm_fields.CharField(max_length=50)

    type: NomenclatureTypes = orm_fields.CharEnumField(NomenclatureTypes, editable=False)
    category: Union["NomenclatureCategory", fields.ForeignKeyRelation["NomenclatureCategory"]] = fields.ForeignKeyField(
        "directories.NomenclatureCategory", related_name='nomenclatures', on_delete=fields.RESTRICT
    )

    units: NomenclatureUnits = orm_fields.CharEnumField(NomenclatureUnits)

    recipe: Union["RecipeCard", fields.BackwardOneToOneRelation["RecipeCard"]]

    stock: Union["NomenclatureStockResult", fields.BackwardOneToOneRelation["NomenclatureStockResult"]]
    cost: Union["NomenclatureCostResult", fields.BackwardOneToOneRelation["NomenclatureCostResult"]]

    class Meta:
        table = "dir__nomenclature"

    def __str__(self) -> str:
        return self.name

    @property
    def cost_value(self) -> Optional[float]:
        return self.cost.cost if self.cost else None

    @property
    def stock_value(self) -> Optional[float]:
        return self.stock.count if self.stock else None
