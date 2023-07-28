from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource,
    nom_type_list_form_primitive,
)
from ..repository import ProvisionRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class ProvisionResource(NomenclatureTypeBaseResource[ProvisionRepository]):
    repository = ProvisionRepository
    list_form_primitive = nom_type_list_form_primitive.copy().add('has_recipe')
