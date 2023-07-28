from typing import TYPE_CHECKING, Union

from tortoise import fields
from core.orm import fields as orm_fields

from core.entities.directories import Directory, DirectoryListValue

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["RecipeCard", "RecipeCardIngredients"]


class RecipeCard(Directory):
    id: int = orm_fields.IntField(pk=True)
    product: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        "directories.Nomenclature", related_name="recipe", on_delete=fields.CASCADE
    )
    text: str = orm_fields.TextField()

    ingredients: list["RecipeCardIngredients"] | fields.BackwardFKRelation["RecipeCardIngredients"]

    class Meta:
        table = "dir__recipe_cards"

    def __str__(self) -> str:
        return str(self.product)


class RecipeCardIngredients(DirectoryListValue):
    card: Union["RecipeCard", fields.ForeignKeyRelation["RecipeCard"]] = fields.ForeignKeyField(
        "directories.RecipeCard", related_name='ingredients', on_delete=fields.CASCADE
    )
    product: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        "directories.Nomenclature", related_name='ingredient_of', on_delete=fields.RESTRICT
    )
    count: float = orm_fields.FloatField(min_value=0)

    class Meta:
        table = "dir__recipe_cards__ingredients"
        ordering = 'ordering',

    def __str__(self) -> str:
        return str(self.product)
