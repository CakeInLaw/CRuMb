from core.admin.forms import Primitive
from core.admin.resources import DirectoryResource

from configuration.admin import CakeInLawAdmin
from configuration.menu_groups import Directories
from .repository import (
    NomenclatureCategoryRepository,
    DishesCategoryRepository,
    HozCategoryRepository,
    InventoryCategoryRepository,
    ProvisionCategoryRepository,
    RawsCategoryRepository,
)


__all__ = ['NomenclatureCategoryResource']


@CakeInLawAdmin.register(
    present_in=(Directories,)
)
class NomenclatureCategoryResource(DirectoryResource[NomenclatureCategoryRepository]):
    repository = NomenclatureCategoryRepository
    list_form_primitive = Primitive('name', 'type')
    create_form_primitive = Primitive('name', 'type')
    edit_form_primitive = Primitive('name')


@CakeInLawAdmin.register()
class DishesCategoryResource(DirectoryResource[DishesCategoryRepository]):
    repository = DishesCategoryRepository
    list_form_primitive = Primitive('name')
    create_form_primitive = Primitive('name')
    edit_form_primitive = Primitive('name')


@CakeInLawAdmin.register()
class HozCategoryResource(DirectoryResource[HozCategoryRepository]):
    repository = HozCategoryRepository
    list_form_primitive = Primitive('name')
    create_form_primitive = Primitive('name')
    edit_form_primitive = Primitive('name')


@CakeInLawAdmin.register()
class InventoryCategoryResource(DirectoryResource[InventoryCategoryRepository]):
    repository = InventoryCategoryRepository
    list_form_primitive = Primitive('name')
    create_form_primitive = Primitive('name')
    edit_form_primitive = Primitive('name')


@CakeInLawAdmin.register()
class ProvisionCategoryResource(DirectoryResource[ProvisionCategoryRepository]):
    repository = ProvisionCategoryRepository
    list_form_primitive = Primitive('name')
    create_form_primitive = Primitive('name')
    edit_form_primitive = Primitive('name')


@CakeInLawAdmin.register()
class RawsCategoryResource(DirectoryResource[RawsCategoryRepository]):
    repository = RawsCategoryRepository
    list_form_primitive = Primitive('name')
    create_form_primitive = Primitive('name')
    edit_form_primitive = Primitive('name')
