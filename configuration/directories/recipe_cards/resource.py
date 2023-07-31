from core.admin.resource import Resource, ListValueResource
from .repository import RecipeCardRepository, RecipeCardIngredientsRepository
from configuration.admin import CakeInLawAdmin

__all__ = ["RecipeCardResource", "RecipeCardIngredientsResource"]


@CakeInLawAdmin.register()
class RecipeCardResource(Resource):
    repository = RecipeCardRepository

    def _methods(self) -> dict[str, ...]:
        return {}


@CakeInLawAdmin.register()
class RecipeCardIngredientsResource(ListValueResource):
    repository = RecipeCardIngredientsRepository
