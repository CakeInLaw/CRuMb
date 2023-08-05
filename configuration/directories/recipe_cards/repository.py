from core.repository import register_repository, ValuesListRepository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import RecipeCard, RecipeCardValuesList


__all__ = ["RecipeCardRepository", "RecipeCardValuesListRepository"]


@register_repository
class RecipeCardRepository(DirectoryRepository[RecipeCard]):
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
class RecipeCardValuesListRepository(ValuesListRepository):
    model = RecipeCardValuesList
    related_repositories = {
        'product': 'RawsAndProvision'
    }

    _t_ru = ru.Entity(
        name='Ингредиент',
        name_plural='Ингредиенты',
    )
    _t_en = en.Entity(
        name='Recipe card',
        name_plural='Recipe cards',
    )
