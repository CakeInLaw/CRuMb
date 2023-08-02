from core.repository import register_repository
from core.entities.directories import DirectoryRepository, DirectoryListValueRepository
from core.translations.langs import ru, en

from .model import RecipeCard, RecipeCardIngredients


__all__ = ["RecipeCardRepository", "RecipeCardIngredientsRepository"]


@register_repository
class RecipeCardRepository(DirectoryRepository):
    model = RecipeCard

    _t_ru = ru.Entity(
        name='Тех. карта',
        name_plural='Тех. карты',
        fields={
            'text': 'Технология приготовления',
        },
    )
    _t_en = en.Entity(
        name='Recipe card',
        name_plural='Recipe cards',
        fields={
            'text': 'Recipe',
        },
    )


@register_repository
class RecipeCardIngredientsRepository(DirectoryListValueRepository):
    model = RecipeCardIngredients

    _t_ru = ru.Entity(
        name='Ингредиент',
        name_plural='Ингредиенты',
        fields={
            'product': 'Продукт',
        },
    )
    _t_en = en.Entity(
        name='Recipe card',
        name_plural='Recipe cards',
        fields={
            'product': 'Product',
        },
    )
