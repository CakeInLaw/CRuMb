from configuration.enums import NomenclatureTypes
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["InventoryRepository"]


class InventoryRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.INVENTORY

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = NomenclatureTranslation.Ru(
        name='Инвентарь',
        name_plural='Инвентарь',
    )
    _TRANSLATION_EN = NomenclatureTranslation.En(
        name='Inventory',
        name_plural='Inventories',
    )
