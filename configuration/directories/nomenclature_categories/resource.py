from admin.forms import Primitive
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import NomenclatureCategoryRepository


__all__ = ['NomenclatureCategoryResource']


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class NomenclatureCategoryResource(Resource[NomenclatureCategoryRepository]):
    repository = NomenclatureCategoryRepository
    list_form_primitive = Primitive('name', 'type')
    create_form_primitive = Primitive('name', 'type')
    edit_form_primitive = Primitive('name')
