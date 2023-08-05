from typing import Optional

from tortoise.queryset import Q

from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from configuration.enums import NomenclatureTypes
from core.types import DATA
from .model import NomenclatureCategory


__all__ = [
    "NomenclatureCategoryRepository",
    "DishesCategoryRepository",
    "HozCategoryRepository",
    "InventoryCategoryRepository",
    "ProvisionCategoryRepository",
    "RawsCategoryRepository",
]


@register_repository
class NomenclatureCategoryRepository(DirectoryRepository[NomenclatureCategory]):
    model = NomenclatureCategory

    _t_ru = ru.Entity(
        name='Категория номенклатуры',
        name_plural='Категории номенклатуры',
        fields={
            'type': 'Вид номенклатуры',
        },
    )
    _t_en = en.Entity(
        name='Nomenclature category',
        name_plural='Nomenclature categories',
        fields={
            'type': 'Nomenclature type',
        },
    )


class NomenclatureTypeCategoryRepository(DirectoryRepository[NomenclatureCategory]):
    type: NomenclatureTypes
    hidden_fields = {'type'}
    model = NomenclatureCategory

    def qs_default_filters(self) -> list[Q]:
        return [Q(type=self.type)]

    @classmethod
    def get_repo_name(cls) -> str:
        return cls.type.name.title()

    async def create(
            self,
            data: DATA,
            *,
            defaults: Optional[DATA] = None,
            is_root: bool = True,
            run_in_transaction: Optional[bool] = None,
            validate: Optional[bool] = None,
    ) -> NomenclatureCategory:
        defaults = defaults or {}
        defaults['type'] = self.type
        return await super().create(
            data=data,
            defaults=defaults,
            is_root=is_root,
            run_in_transaction=run_in_transaction,
            validate=validate,
        )


@register_repository
class DishesCategoryRepository(NomenclatureTypeCategoryRepository):
    type = NomenclatureTypes.DISHES
    _t_ru = ru.Entity(
        name='Категория блюд',
        name_plural='Категории блюд',
    )
    _t_en = en.Entity(
        name='Dishes category',
        name_plural='Dishes categories',
    )


@register_repository
class HozCategoryRepository(NomenclatureTypeCategoryRepository):
    type = NomenclatureTypes.HOZ
    _t_ru = ru.Entity(
        name='Категория хозтоваров',
        name_plural='Категории хозтоваров',
    )
    _t_en = en.Entity(
        name='Household goods category',
        name_plural='Household goods categories',
    )


@register_repository
class InventoryCategoryRepository(NomenclatureTypeCategoryRepository):
    type = NomenclatureTypes.INVENTORY
    _t_ru = ru.Entity(
        name='Категория инвентаря',
        name_plural='Категории инвентаря',
    )
    _t_en = en.Entity(
        name='Inventory category',
        name_plural='Inventory categories',
    )


@register_repository
class ProvisionCategoryRepository(NomenclatureTypeCategoryRepository):
    type = NomenclatureTypes.PROVISION
    _t_ru = ru.Entity(
        name='Категория заготовок',
        name_plural='Категории заготовок',
    )
    _t_en = en.Entity(
        name='Provision category',
        name_plural='Provision categories',
    )


@register_repository
class RawsCategoryRepository(NomenclatureTypeCategoryRepository):
    type = NomenclatureTypes.RAWS
    _t_ru = ru.Entity(
        name='Категория продуктов',
        name_plural='Категории продуктов',
    )
    _t_en = en.Entity(
        name='Products category',
        name_plural='Products categories',
    )
