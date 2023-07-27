from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ...models import Nomenclature


__all__ = ["NomenclatureRepository"]


@default_repository
class NomenclatureRepository(DirectoryRepository):
    model = Nomenclature

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Номенклатура',
        name_plural='Номенклатура',
        fields={
            'type': 'Вид номенклатуры',
            'category': 'Категория',
            'units': 'Ед. измерения',
            'stock': 'Остаток',
            'cost': 'Себестоимость',
            'price': 'Цена',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Nomenclature',
        name_plural='Nomenclature',
        fields={
            'type': 'Type',
            'category': 'Category',
            'units': 'Units',
            'stock': 'Stock',
            'cost': 'Cost',
            'price': 'Price',
        },
    )
