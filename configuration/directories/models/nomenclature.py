from typing import TYPE_CHECKING, Union, Optional

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory
from configuration.enums import NomenclatureTypes, NomenclatureUnits

if TYPE_CHECKING:
    from configuration.directories.models import RecipeCard, RecipeCardIngredients
    from configuration.accum_registers.models import NomenclatureStock, NomenclatureStockResult
    from configuration.info_registers.models import NomenclatureCost, NomenclaturePrice


__all__ = ["Nomenclature"]


class Nomenclature(Directory):
    id: int = fields.BigIntField(pk=True)

    name: str = orm_fields.CharField(max_length=50)

    type: NomenclatureTypes = fields.CharEnumField(NomenclatureTypes, max_length=1)

    units: NomenclatureUnits = fields.CharEnumField(NomenclatureUnits, max_length=1)

    recipe: Union["RecipeCard", fields.BackwardOneToOneRelation["RecipeCard"]]
    ingredient_of: list["RecipeCardIngredients"] | fields.BackwardFKRelation["RecipeCardIngredients"]

    stock_history: list["NomenclatureStock"] | fields.BackwardFKRelation["NomenclatureStock"]
    stock: Union["NomenclatureStockResult", fields.BackwardOneToOneRelation["NomenclatureStockResult"]]
    stock_count: float  # annotated

    costs: list["NomenclatureCost"] | fields.BackwardFKRelation["NomenclatureCost"]
    cost: float  # annotated
    prices: list["NomenclaturePrice"] | fields.BackwardFKRelation["NomenclaturePrice"]

    class Meta:
        table = "dir__nomenclature"
        ordering = ('id',)

    def __str__(self) -> str:
        return self.name
