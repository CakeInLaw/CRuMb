from core.admin.forms import Primitive
from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource,
    nom_type_list_form_primitive,
    nom_type_create_form_primitive,
    nom_type_edit_form_primitive,
    RecipeInputSchema
)
from ..repository import DishesRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class DishesResource(NomenclatureTypeBaseResource[DishesRepository]):
    repository = DishesRepository
    list_form_primitive = nom_type_list_form_primitive.copy()
    create_form_primitive = nom_type_create_form_primitive.copy().add(RecipeInputSchema)
    edit_form_primitive = nom_type_edit_form_primitive.copy().add(RecipeInputSchema)
