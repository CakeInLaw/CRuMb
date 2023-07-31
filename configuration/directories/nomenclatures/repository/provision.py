from configuration.enums import NomenclatureTypes
from core.enums import FieldTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["ProvisionRepository"]


@register_repository
class ProvisionRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.PROVISION
    calculated = {'has_recipe': FieldTypes.BOOL}

    _t_ru = NomenclatureTranslation.Ru(
        name='Заготовка',
        name_plural='Заготовки',
    )
    _t_en = NomenclatureTranslation.En(
        name='Provision',
        name_plural='Provision',
    )

    def qs_select_related(self) -> set[str]:
        return {*super().qs_select_related(), 'recipe'}
