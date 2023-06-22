from typing import TYPE_CHECKING, Union, Optional

from tortoise import fields

from core.entities.directories.model import Directory
from configuration.enums import NomenclatureTypes, NomenclatureUnits

if TYPE_CHECKING:
    from configuration.directories.models import RecipeCard, RecipeCardIngredients
    from configuration.accum_registers.models import NomenclatureStock, NomenclatureStockResult
    from configuration.info_registers.models import NomenclatureCost, NomenclaturePrice


__all__ = ["Nomenclature"]


class Nomenclature(Directory):
    id: int = fields.BigIntField(pk=True)

    name: str = fields.CharField(max_length=50)
    child_name: str = fields.CharField(max_length=50)
    full_name: str = fields.CharField(max_length=300)

    type: NomenclatureTypes = fields.CharEnumField(NomenclatureTypes, max_length=1)

    is_group: bool = fields.BooleanField()
    parent: Union["Nomenclature", fields.ForeignKeyNullableRelation["Nomenclature"]] = fields.ForeignKeyField(
        'directories.Nomenclature', related_name='children', on_delete=fields.RESTRICT, null=True
    )
    children: list["Nomenclature"] | fields.BackwardFKRelation["Nomenclature"]

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

    def update_full_name(self, parent: Optional["Nomenclature"] = None) -> None:
        parent = parent or self.parent
        if not parent:
            self.full_name = self.name.capitalize()
        else:
            self.full_name = f'{parent.full_name} {self.name}'.strip().capitalize()
