from core.admin.forms import Primitive
from core.admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import CustomerLocationRepository


__all__ = ["CustomerLocationResource"]


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class CustomerLocationResource(Resource):
    repository = CustomerLocationRepository
    list_form_primitive = Primitive('customer_id', 'name', 'delivery_address')
    form_primitive = Primitive(
        'name',
        'delivery_address',
        'customer_id'
    )
