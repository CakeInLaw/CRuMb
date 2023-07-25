from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import PriceGroupRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Prices, Sells


@CakeInLawAdmin.register(
    present_in=(Prices, Sells)
)
class PriceGroupResource(Resource):
    repository = PriceGroupRepository
    list_primitive = Primitive('name')
    form_primitive = Primitive('name')
