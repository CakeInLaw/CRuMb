from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import CustomerLocation


__all__ = ["CustomerLocationRepository"]


@register_repository
class CustomerLocationRepository(DirectoryRepository[CustomerLocation]):
    model = CustomerLocation

    _t_ru = ru.Entity(
        name='Точка покупателя',
        name_plural='Точки покупателей',
        fields={
            'delivery_address': 'Адрес доставки',
        }
    )
    _t_en = en.Entity(
        name='Customer location',
        name_plural='Customer locations',
        fields={
            'delivery_address': 'Delivery address',
        }
    )

    def qs_select_related(self) -> set[str]:
        return {'customer'}
