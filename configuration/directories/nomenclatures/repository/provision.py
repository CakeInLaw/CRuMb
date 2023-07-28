from configuration.enums import NomenclatureTypes
from core.enums import FieldTypes
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["ProvisionRepository"]


class ProvisionRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.PROVISION
    calculated = {'has_recipe': FieldTypes.BOOL}

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = NomenclatureTranslation.Ru(
        name='Заготовка',
        name_plural='Заготовки',
    )
    _TRANSLATION_EN = NomenclatureTranslation.En(
        name='Provision',
        name_plural='Provision',
    )

    def qs_select_related(self) -> set[str]:
        return {*super().qs_select_related(), 'recipe'}
