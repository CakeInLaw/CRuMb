from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from .model import Provider


__all__ = ["ProviderRepository"]


@register_repository
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
