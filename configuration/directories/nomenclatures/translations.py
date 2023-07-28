from core.translations import Translation


class NomenclatureTranslationRu(Translation.Ru):
    def __init__(
            self,
            name: str,
            name_plural: str,
            create: str = None,
            edit: str = None
    ):
        super().__init__(
            name=name,
            name_plural=name_plural,
            create=create,
            edit=edit,
            fields={
                'type': 'Вид номенклатуры',
                'category': 'Категория',
                'units': 'Ед. измерения',
                'stock': 'Остаток',
                'cost': 'Себестоимость',
                'price': 'Цена',
                'has_recipe': 'Есть техкарта',
            },
        )


class NomenclatureTranslationEn(Translation.En):
    def __init__(
            self,
            name: str,
            name_plural: str,
            create: str = None,
            edit: str = None
    ):
        super().__init__(
            name=name,
            name_plural=name_plural,
            create=create,
            edit=edit,
            fields={
                'type': 'Type',
                'category': 'Category',
                'units': 'Units',
                'stock': 'Stock',
                'cost': 'Cost',
                'price': 'Price',
                'has_recipe': 'Has recipe',
            },
        )


class NomenclatureTranslation:
    Ru = NomenclatureTranslationRu
    En = NomenclatureTranslationEn
