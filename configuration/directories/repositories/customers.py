from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import Customer


__all__ = ["CustomerRepository"]


@default_repository
class CustomerRepository(DirectoryRepository):
    model = Customer

    _TRANSLATION_RU = {
        'name': 'Покупатель',
        'name_plural': 'Покупатели',
        'fields': {
            'name': 'Наименование',
            'register_address': 'Адрес регистрации',
        },
    }
