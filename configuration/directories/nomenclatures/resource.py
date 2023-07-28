from admin.forms import Primitive
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import NomenclatureRepository


@CakeInLawAdmin.register(
    present_in=(Directories, )
)
class NomenclatureResource(Resource):
    repository = NomenclatureRepository
    list_form_primitive = Primitive('category_id', 'name', 'units', 'has_recipe')
    form_primitive = Primitive('name', )
