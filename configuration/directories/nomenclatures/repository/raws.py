from configuration.enums import NomenclatureTypes
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["RawsRepository"]


class RawsRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.RAWS

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = NomenclatureTranslation.Ru(
        name='Продукт',
        name_plural='Продукты',
    )
    _TRANSLATION_EN = NomenclatureTranslation.En(
        name='Raws',
        name_plural='Raws',
    )
