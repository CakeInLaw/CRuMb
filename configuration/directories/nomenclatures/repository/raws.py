from configuration.enums import NomenclatureTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["RawsRepository"]


@register_repository
class RawsRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.RAWS

    _t_ru = NomenclatureTranslation.Ru(
        name='Продукт',
        name_plural='Продукты',
    )
    _t_en = NomenclatureTranslation.En(
        name='Product',
        name_plural='Products',
    )
