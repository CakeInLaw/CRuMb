from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import TranslationRu, TranslationEn

from ..models import Customer


__all__ = ["CustomerRepository"]


@default_repository
class CustomerRepository(DirectoryRepository):
    model = Customer

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = TranslationRu(
        name='Покупатель',
        name_plural='Покупатели',
        fields={
            'register_address': 'Адрес регистрации',
        },
    )
    _TRANSLATION_EN = TranslationEn(
        name='Customer',
        name_plural='Customers',
        fields={
            'register_address': 'Register address',
        },
    )

    def qs_select_related(self) -> set[str]:
        if self.by == 'admin' and self.extra['target'] == 'edit':
            return {'price_group'}
        return set()
