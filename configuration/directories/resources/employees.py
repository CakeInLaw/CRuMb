from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import EmployeeRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


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
