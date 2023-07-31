from configuration.enums import NomenclatureTypes
from core.enums import FieldTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["DishesRepository"]


@register_repository
class DishesRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.DISHES

    _t_ru = NomenclatureTranslation.Ru(
        name='Блюдо',
        name_plural='Блюда',
    )
    _t_en = NomenclatureTranslation.En(
        name='Dish',
        name_plural='Dishes',
    )

    def qs_select_related(self) -> set[str]:
        return {*super().qs_select_related(), 'recipe'}
