from admin.forms import Primitive
from admin.resource import Resource, ListValueResource
from .repository import RecipeCardRepository, RecipeCardIngredientsRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


__all__ = ["RecipeCardResource", "RecipeCardIngredientsResource"]


@CakeInLawAdmin.register()
class RecipeCardResource(Resource):
    repository = RecipeCardRepository

    def _methods(self) -> dict[str, ...]:
        return {}


@CakeInLawAdmin.register()
class RecipeCardIngredientsResource(ListValueResource):
    repository = RecipeCardIngredientsRepository
