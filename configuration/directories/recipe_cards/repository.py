from core.repository import default_repository
from core.entities.directories import DirectoryRepository, DirectoryValueRepository
from core.translations import Translation

from .model import RecipeCard, RecipeCardIngredients


__all__ = ["RecipeCardRepository", "RecipeCardIngredientsRepository"]


@default_repository
class RecipeCardRepository(DirectoryRepository):
    model = RecipeCard

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Тех. карта',
        name_plural='Тех. карты',
        fields={
            'text': 'Рецепт',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Recipe card',
        name_plural='Recipe cards',
        fields={
            'text': 'Recipe',
        },
    )


@default_repository
class RecipeCardIngredientsRepository(DirectoryValueRepository):
    model = RecipeCardIngredients

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Ингредиент',
        name_plural='Ингредиенты',
        fields={
            'product': 'Продукт',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Recipe card',
        name_plural='Recipe cards',
        fields={
            'product': 'Product',
        },
    )
