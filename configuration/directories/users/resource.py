from admin.forms import Primitive
from admin.forms.widgets import StrInput
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import UserRepository


__all__ = ["UserResource"]


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class UserResource(Resource):
    repository = UserRepository
    list_form_primitive = Primitive('username', 'created_at')
    create_form_primitive = Primitive(
        'username',
        StrInput(name='password', required=False, is_password=True, empty_as_none=True, ignore_if_none=True),
        StrInput(name='re_password', required=False, is_password=True, empty_as_none=True, ignore_if_none=True)
    )
    edit_form_primitive = Primitive(
        'username',
        'created_at',
    )
