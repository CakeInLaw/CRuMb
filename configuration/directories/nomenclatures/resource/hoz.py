from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Nomenclature
from .default import (
    NomenclatureTypeBaseResource,
)
from ..repository import HozRepository


@CakeInLawAdmin.register(
    present_in=(Nomenclature, )
)
class HozResource(NomenclatureTypeBaseResource[HozRepository]):
    repository = HozRepository
