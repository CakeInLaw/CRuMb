from configuration.enums import NomenclatureTypes, NomenclatureUnits, OperationTypes
from core.translations.app_translation import AppTranslation
from core.translations.langs import ru, en


app_translations = AppTranslation(
    ru=ru.interface,
    en=en.interface
)

app_translations.add_enum(
    NomenclatureTypes,
    ru={
        NomenclatureTypes.HOZ: 'Хозтовары',
        NomenclatureTypes.INVENTORY: 'Инвентарь',
        NomenclatureTypes.RAWS: 'Продукты',
        NomenclatureTypes.PROVISION: 'Заготовки',
        NomenclatureTypes.DISHES: 'Блюда',
    },
    en={
        NomenclatureTypes.HOZ: 'Household goods',
        NomenclatureTypes.INVENTORY: 'Inventory',
        NomenclatureTypes.RAWS: 'Progucts',
        NomenclatureTypes.PROVISION: 'Provision',
        NomenclatureTypes.DISHES: 'Dishes',
    }
)
app_translations.add_enum(
    NomenclatureUnits,
    ru={
        NomenclatureUnits.UNITS: 'Штуки',
        NomenclatureUnits.KILOGRAMS: 'Килограммы',
        NomenclatureUnits.LITERS: 'Литры',
        NomenclatureUnits.CENTIMETERS: 'Сантиметры',
        NomenclatureUnits.METERS: 'Метры',
    },
    en={
        NomenclatureUnits.UNITS: 'Units',
        NomenclatureUnits.KILOGRAMS: 'Kilograms',
        NomenclatureUnits.LITERS: 'Liters',
        NomenclatureUnits.CENTIMETERS: 'Centimeters',
        NomenclatureUnits.METERS: 'Meters',
    }
)
app_translations.add_enum(
    OperationTypes,
    ru={
        OperationTypes.WRITE_OFF: 'Списание'
    },
    en={
        OperationTypes.WRITE_OFF: 'Write off',
    }
)
