from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import UserRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import System


@CakeInLawAdmin.register(
    present_in=(System,)
)
class UserResource(Resource):
    repository = UserRepository
    list_primitive = Primitive('username', 'created_at')
    form_primitive = Primitive('username')
