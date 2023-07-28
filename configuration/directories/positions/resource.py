from admin.forms import Primitive
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import PositionRepository


__all__ = ["PositionResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PositionResource(Resource):
    repository = PositionRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name')
