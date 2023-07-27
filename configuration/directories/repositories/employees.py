from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.translations import Translation

from ..models import Employee


__all__ = ["EmployeeRepository"]


@default_repository
class EmployeeRepository(DirectoryRepository):
    model = Employee

    _TRANSLATION_DEFAULT = _TRANSLATION_RU = Translation.Ru(
        name='Сотрудник',
        name_plural='Сотрудники',
        fields={
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'fathers_name': 'Отчество',
        },
    )
    _TRANSLATION_EN = Translation.En(
        name='Employee',
        name_plural='Employees',
        fields={
            'last_name': 'Last name',
            'first_name': 'First name',
            'fathers_name': 'Patronymic',
        },
    )

    def qs_select_related(self) -> set[str]:
        return {'position'}
