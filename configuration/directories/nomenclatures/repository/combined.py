from tortoise.queryset import Q

from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from configuration.enums import NomenclatureTypes as Nt
from ..model import Nomenclature
from ..translations import NomenclatureTranslation


class CombinedNomenclatureTypeRepository(DirectoryRepository[Nomenclature]):
    model = Nomenclature
    READ_ONLY_REPOSITORY = True
    types: tuple[Nt]

    def qs_default_filters(self) -> list[Q]:
        return [Q(*[Q(type=t) for t in self.types], join_type=Q.OR)]


@register_repository
class IngredientRepository(CombinedNomenclatureTypeRepository):
    _REPOSITORY_NAME = 'Ingredients'
    types = (Nt.RAWS, Nt.PROVISION)

    _t_ru = NomenclatureTranslation.Ru(
        name='Ингредиент',
        name_plural='Ингредиенты',
    )
    _t_en = NomenclatureTranslation.En(
        name='Ingredient',
        name_plural='Ingredients',
    )


@register_repository
class AssembledRepository(CombinedNomenclatureTypeRepository):
    _REPOSITORY_NAME = 'Assembled'
    types = (Nt.PROVISION, Nt.DISHES)

    _t_ru = NomenclatureTranslation.Ru(
        name='Заготовка или блюдо',
        name_plural='Заготовки и блюда',
    )
    _t_en = NomenclatureTranslation.En(
        name='Provision or dish',
        name_plural='Provision and dishes',
    )


@register_repository
class ReceivedRepository(CombinedNomenclatureTypeRepository):
    _REPOSITORY_NAME = 'Received'
    types = (Nt.INVENTORY, Nt.HOZ, Nt.RAWS)

    _t_ru = NomenclatureTranslation.Ru(
        name='Номенклатура',
        name_plural='Номенклатура',
    )
    _t_en = NomenclatureTranslation.En(
        name='Nomenclature',
        name_plural='Nomenclatures',
    )


@register_repository
class SellableRepository(CombinedNomenclatureTypeRepository):
    _REPOSITORY_NAME = 'Sellable'
    types = (Nt.DISHES, )

    _t_ru = NomenclatureTranslation.Ru(
        name='Блюдо',
        name_plural='Блюда',
    )
    _t_en = NomenclatureTranslation.En(
        name='Dish',
        name_plural='Dishes',
    )
