from admin.resource import Resource
from configuration.admin import CakeInLawAdmin
from ..repositories import PriceGroupRepository


@CakeInLawAdmin.register()
class PriceGroupResource(Resource):
    repository = PriceGroupRepository
    datagrid_columns = ['name']
