from core.repository import default_repository
from core.entities.directories import DirectoryRepository, DirectoryValueRepository

from ..models import RecipeCard, RecipeCardIngredients


__all__ = ["RecipeCardRepository", "RecipeCardIngredientsRepository"]


@default_repository
class RecipeCardRepository(DirectoryRepository):
    model = RecipeCard


@default_repository
class RecipeCardIngredientsRepository(DirectoryValueRepository):
    model = RecipeCardIngredients
