from core.admin.app import CRuMbAdmin
from . import menu_groups


class CakeInLawAdmin(CRuMbAdmin):
    title: str = 'CakeInLaw'
    menu_groups = [*menu_groups.roots]
