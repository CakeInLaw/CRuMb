from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import Customer


__all__ = ["CustomerRepository"]


@register_repository
class CustomerRepository(DirectoryRepository):
    model = Customer

    _t_ru = ru.Entity(
        name='Покупатель',
        name_plural='Покупатели',
        fields={
            'register_address': 'Адрес регистрации',
        },
    )
    _t_en = en.Entity(
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
