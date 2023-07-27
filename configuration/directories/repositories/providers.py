from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ..models import Provider


__all__ = ["ProviderRepository"]


@default_repository
class ProviderRepository(DirectoryRepository):
    model = Provider

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Поставщик',
        name_plural='Поставщики',
        fields={
            'register_address': 'Адрес регистрации',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Provider',
        name_plural='Providers',
        fields={
            'register_address': 'Register address',
        },
    )
