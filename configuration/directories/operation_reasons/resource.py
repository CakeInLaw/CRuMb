from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import OperationReasonRepository


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class OperationReasonResource(DirectoryResource[OperationReasonRepository]):
    repository = OperationReasonRepository
    list_form_primitive = Primitive('name', 'operation_type')
    create_form_primitive = Primitive('name', 'operation_type')
    edit_form_primitive = Primitive('name')
