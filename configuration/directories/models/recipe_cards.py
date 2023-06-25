from typing import TYPE_CHECKING, Union

from tortoise import fields

from core.entities.directories.model import Directory

if TYPE_CHECKING:
    from configuration.directories.models import Nomenclature


__all__ = ["RecipeCard", "RecipeCardIngredients"]


class RecipeCard(Directory):
    id: int = fields.IntField(pk=True)
    product: Union["Nomenclature", fields.OneToOneRelation["Nomenclature"]] = fields.OneToOneField(
        "directories.Nomenclature", related_name="recipe", on_delete=fields.CASCADE
    )
    text: str = fields.TextField()

    ingredients: list["RecipeCardIngredients"] | fields.BackwardFKRelation["RecipeCardIngredients"]

    class Meta:
        table = "dir__recipe_cards"


class RecipeCardIngredients(Directory):
    id: int = fields.BigIntField(pk=True)
    order: int = fields.SmallIntField()
    product: Union["Nomenclature", fields.ForeignKeyRelation["Nomenclature"]] = fields.ForeignKeyField(
        "directories.Nomenclature", related_name='ingredient_of', on_delete=fields.RESTRICT
    )
    recipe: Union["RecipeCard", fields.ForeignKeyRelation["RecipeCard"]] = fields.ForeignKeyField(
        "directories.RecipeCard", related_name="ingredients", on_delete=fields.CASCADE
    )

    class Meta:
        table = "dir__recipe_cards__ingredients"
        ordering = ('order',)
        unique_together = ('product', 'recipe')
