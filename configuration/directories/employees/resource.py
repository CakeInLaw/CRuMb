from core.admin.forms import Primitive
from core.admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import EmployeeRepository


__all__ = ["EmployeeResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class EmployeeResource(Resource):
    repository = EmployeeRepository
    list_form_primitive = Primitive(
        'last_name',
        'first_name',
        'fathers_name',
        'position_id',
    )
    form_primitive = Primitive(
        'last_name',
        'first_name',
        'fathers_name',
        'position_id',
    )
