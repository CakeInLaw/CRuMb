from admin.forms import Primitive
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import PriceGroupRepository


__all__ = ["PriceGroupResource"]


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PriceGroupResource(Resource):
    repository = PriceGroupRepository
    list_form_primitive = Primitive('name')
    form_primitive = Primitive('name')
