from configuration.enums import NomenclatureTypes
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["HozRepository"]


class HozRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.HOZ

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = NomenclatureTranslation.Ru(
        name='Хозтовар',
        name_plural='Хозтовары',
    )
    _TRANSLATION_EN = NomenclatureTranslation.En(
        name='household good',
        name_plural='household goods',
    )
