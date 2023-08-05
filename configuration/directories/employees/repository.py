from core.repository import register_repository
from core.entities.directories import DirectoryRepository
from core.translations.langs import ru, en

from .model import Employee


__all__ = ["EmployeeRepository"]


@register_repository
class EmployeeRepository(DirectoryRepository[Employee]):
    model = Employee

    _t_ru = ru.Entity(
        name='Сотрудник',
        name_plural='Сотрудники',
        fields={
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'fathers_name': 'Отчество',
        },
    )
    _t_en = en.Entity(
        name='Employee',
        name_plural='Employees',
        fields={
            'last_name': 'Last name',
            'first_name': 'First name',
            'fathers_name': 'Patronymic',
        },
    )

    def qs_select_related(self) -> tuple[str]:
        return 'position',
