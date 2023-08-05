from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import Provider


__all__ = ["ProviderRepository"]


@register_repository
class ProviderRepository(DirectoryRepository[Provider]):
    model = Provider

    _t_ru = ru.Entity(
        name='Поставщик',
        name_plural='Поставщики',
        fields={
            'register_address': 'Адрес регистрации',
        },
    )
    _t_en = en.Entity(
        name='Provider',
        name_plural='Providers',
        fields={
            'register_address': 'Register address',
        },
    )
