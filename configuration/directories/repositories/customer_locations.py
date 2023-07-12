from typing import Any

from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import CustomerLocation


__all__ = ["CustomerLocationRepository"]


@default_repository
class CustomerLocationRepository(DirectoryRepository):
    model = CustomerLocation

    _TRANSLATION_RU = {
        'name': 'Точка покупателя',
        'name_plural': 'Точки покупателей',
        'fields': {
            'name': 'Наименование',
            'order': 'Порядок',
            'delivery_address': 'Адрес доставки',
            'customer': 'Покупатель',
            'customer_id': 'Покупатель',
        }
    }

    def qs_select_related(self) -> set[str]:
        return {'user', 'customer'}
