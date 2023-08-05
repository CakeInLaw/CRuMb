from core.admin.resources import DirectoryResource, ValuesListResource
from .repository import RecipeCardRepository, RecipeCardValuesListRepository
from configuration.admin import CakeInLawAdmin

__all__ = ["RecipeCardResource", "RecipeCardValuesListResource"]


@CakeInLawAdmin.register()
class RecipeCardResource(DirectoryResource[RecipeCardRepository]):
    repository = RecipeCardRepository

    def _methods(self) -> dict[str, ...]:
        return {}


@CakeInLawAdmin.register()
class RecipeCardValuesListResource(ValuesListResource):
    repository = RecipeCardValuesListRepository
