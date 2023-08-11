from typing import ClassVar, Type

from core.admin.app import CRuMbAdmin
from core.admin.layout import MenuGroup

from . import menu_groups


class CakeInLawAdmin(CRuMbAdmin):
    title: ClassVar[str] = 'CakeInLaw'
    menu_groups: ClassVar[list[Type[MenuGroup]]] = [*menu_groups.roots]
