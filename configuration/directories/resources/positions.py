from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import PositionRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PositionResource(Resource):
    repository = PositionRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name')
