from admin.forms import Primitive
from admin.resource import Resource

from ..repositories import NomenclatureRepository
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class PositionResource(Resource):
    repository = NomenclatureRepository
    list_form_primitive = Primitive('category', 'name', 'units', 'has_recipe')
    form_primitive = Primitive('name', )
