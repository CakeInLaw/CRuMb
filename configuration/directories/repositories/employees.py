from core.repository import default_repository
from core.entities.directories import DirectoryRepository

from ..models import Employee


__all__ = ["EmployeeRepository"]


@default_repository
class EmployeeRepository(DirectoryRepository):
    model = Employee
