from admin.resource import Resource

from ..repositories import CustomerLocationRepository
from configuration.menu_groups import Sells
from configuration.admin import CakeInLawAdmin


@CakeInLawAdmin.register
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    datagrid_columns = ['order', 'customer']
    present_in = (Sells,)
