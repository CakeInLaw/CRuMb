from admin.resource import Resource

from ..repositories import PriceGroupRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Prices, Sells


@CakeInLawAdmin.register
class PriceGroupResource(Resource):
    repository = PriceGroupRepository
    datagrid_columns = ['name']
    present_in = (Prices, Sells)
