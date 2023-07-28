from typing import TypeVar

from admin.forms import Primitive
from admin.resource import Resource

from configuration.admin import CakeInLawAdmin
from ..repository import NomenclatureRepository
from ..repository.default import NomenclatureTypeBaseRepository


@CakeInLawAdmin.register()
class NomenclatureResource(Resource[NomenclatureRepository]):
    repository = NomenclatureRepository
    list_form_primitive = Primitive('name', 'type', 'category_id', 'units')


nom_type_list_form_primitive = Primitive('name', 'category_id', 'units')
nom_type_choice_form_primitive = Primitive('name', 'category_id', 'units')
nom_type_create_form_primitive = Primitive('name', 'category_id', 'units')
nom_type_edit_form_primitive = Primitive('name', 'category_id', 'units')
R = TypeVar('R', bound=NomenclatureTypeBaseRepository)


class NomenclatureTypeBaseResource(Resource[R]):
    list_form_primitive = nom_type_list_form_primitive
    choice_form_primitive = nom_type_choice_form_primitive
    create_form_primitive = nom_type_create_form_primitive
    edit_form_primitive = nom_type_edit_form_primitive
