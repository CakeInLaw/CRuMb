from typing import Optional, cast

from tortoise.queryset import Q

from configuration.enums import NomenclatureTypes
from core.exceptions import AnyFieldError
from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.types import DATA, PK, MODEL

from ...models import NomenclatureCategory, Nomenclature
from ..translations import NomenclatureTranslation


__all__ = ["NomenclatureRepository", "NomenclatureTypeBaseRepository"]


@register_repository
class NomenclatureRepository(DirectoryRepository[Nomenclature]):
    READ_ONLY_REPOSITORY = True
    model = Nomenclature

    _t_ru = NomenclatureTranslation.Ru(
        name='Номенклатура',
        name_plural='Номенклатура',
    )
    _t_en = NomenclatureTranslation.En(
        name='Nomenclature',
        name_plural='Nomenclature',
    )


InvalidCategoryType = AnyFieldError(
    'invalid_category_type',
    'Вид номенклатуры категории не совпадает с таковым для номенклатуры'
)


class NomenclatureTypeBaseRepository(DirectoryRepository[Nomenclature]):
    type: NomenclatureTypes
    model = Nomenclature
    hidden_fields = {'type'}

    def qs_default_filters(self) -> list[Q]:
        return [Q(type=self.type)]

    @classmethod
    def get_repo_name(cls):
        return cls.type.name.title()

    @classmethod
    def get_related_repositories(cls) -> dict[str, str]:
        return {'category': cls.type.name.title()}

    async def get_create_defaults(self, data: DATA, user_defaults: Optional[DATA]) -> DATA:
        defaults = user_defaults or {}
        defaults['type'] = self.type
        return defaults

    async def _validate_category_id(
            self,
            value: PK,
            data: DATA,
    ) -> None:
        category = cast(NomenclatureCategory, await self.validate_fk_pk(
            field_name='category_id',
            value=value,
            data=data,
        ))
        if category and category.type != self.type:
            raise InvalidCategoryType
