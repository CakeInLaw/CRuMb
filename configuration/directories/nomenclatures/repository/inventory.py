from configuration.enums import NomenclatureTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["InventoryRepository"]


@register_repository
class InventoryRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.INVENTORY

    _t_ru = NomenclatureTranslation.Ru(
        name='Инвентарь',
        name_plural='Инвентарь',
    )
    _t_en = NomenclatureTranslation.En(
        name='Inventory',
        name_plural='Inventories',
    )
