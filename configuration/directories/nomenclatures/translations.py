from dataclasses import dataclass, field

from core.translations.langs import ru, en


@dataclass
class NomenclatureTranslationRu(ru.Entity):
    fields: dict[str, str] = field(default_factory=lambda: {
        'type': 'Вид номенклатуры',
        'category': 'Категория',
        'units': 'Ед. измерения',
        'stock_value': 'Остаток',
        'cost_value': 'Себестоимость',
        'price_value': 'Цена',
    })


@dataclass
class NomenclatureTranslationEn(en.Entity):
    fields: dict[str, str] = field(default_factory=lambda: {
        'type': 'Type',
        'category': 'Category',
        'units': 'Units',
        'stock_value': 'Stock',
        'cost_value': 'Cost',
        'price_value': 'Price',
    })


class NomenclatureTranslation:
    Ru = NomenclatureTranslationRu
    En = NomenclatureTranslationEn
