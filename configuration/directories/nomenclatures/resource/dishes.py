from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource as Parent,
    RecipeInputSchema
)
from ..repository import DishesRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class DishesResource(Parent[DishesRepository]):
    repository = DishesRepository
    create_form_primitive = Parent.create_form_primitive.copy().add(RecipeInputSchema)
    edit_form_primitive = Parent.edit_form_primitive.copy().add(RecipeInputSchema)

    edit_select_related = ('recipe', )
    edit_prefetch_related = ('recipe__values_list__product',)

