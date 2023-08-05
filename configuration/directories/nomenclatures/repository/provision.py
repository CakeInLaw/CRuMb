from configuration.enums import NomenclatureTypes
from core.repository import register_repository
from .default import NomenclatureTypeBaseRepository
from ..translations import NomenclatureTranslation


__all__ = ["ProvisionRepository"]


@register_repository
class ProvisionRepository(NomenclatureTypeBaseRepository):
    type = NomenclatureTypes.PROVISION

    _t_ru = NomenclatureTranslation.Ru(
        name='Заготовка',
        name_plural='Заготовки',
    )
    _t_en = NomenclatureTranslation.En(
        name='Provision',
        name_plural='Provision',
    )
