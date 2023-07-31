from core.admin.forms import Primitive
from core.admin.resource import Resource
from .repository import OperationReasonRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class OperationReasonResource(Resource):
    repository = OperationReasonRepository
    list_form_primitive = Primitive('name', 'operation_type')
    create_form_primitive = Primitive('name', 'operation_type')
    edit_form_primitive = Primitive('name')
