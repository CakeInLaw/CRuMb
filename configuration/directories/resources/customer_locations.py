from admin.resource import Resource
from configuration.admin import CakeInLawAdmin

from ..repositories import CustomerLocationRepository


@CakeInLawAdmin.register()
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    datagrid_columns = ['order', 'customer']
