from configuration.enums import NomenclatureTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["HozRepository"]


@register_repository
class HozRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.HOZ

    _t_ru = NomenclatureTranslation.Ru(
        name='Хозтовар',
        name_plural='Хозтовары',
    )
    _t_en = NomenclatureTranslation.En(
        name='Household good',
        name_plural='Household goods',
    )
