from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from .model import Customer


__all__ = ["CustomerRepository"]


@default_repository
class CustomerRepository(DirectoryRepository):
    model = Customer

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Покупатель',
        name_plural='Покупатели',
        fields={
            'register_address': 'Адрес регистрации',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Customer',
        name_plural='Customers',
        fields={
            'register_address': 'Register address',
        },
    )

    def qs_select_related(self) -> set[str]:
        return {'price_group'}

    def qs_prefetch_related(self) -> set[str]:
        if self.extra.get('target') == 'edit':
            return {'customer_locations'}
        return set()
