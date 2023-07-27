from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ..models import CustomerLocation


__all__ = ["CustomerLocationRepository"]


@default_repository
class CustomerLocationRepository(DirectoryRepository):
    model = CustomerLocation

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Точка покупателя',
        name_plural='Точки покупателей',
        fields={
            'delivery_address': 'Адрес доставки',
        }
    )
    _TRANSLATION_EN = Translation.En(
        name='Customer location',
        name_plural='Customer locations',
        fields={
            'delivery_address': 'Delivery address',
        }
    )

    def qs_select_related(self) -> set[str]:
        return {'user', 'customer'}
