from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import PriceGroup


__all__ = ["PriceGroupRepository"]


@default_repository
class PriceGroupRepository(DirectoryRepository):
    model = PriceGroup

    _TRANSLATION_RU = {
        'name': 'Ценовая группа',
        'name_plural': 'Ценовые группы',
        'fields': {
            'name': 'Наименование',
        },
    }
