from flet import icons

from core.admin.layout import MenuGroup


class Nomenclature(MenuGroup):
    icon = icons.LIBRARY_BOOKS_OUTLINED
    label = 'Номенклатура'


class Directories(MenuGroup):
    icon = icons.LIBRARY_BOOKS_OUTLINED
    label = 'Справочники'
    subgroups = [Nomenclature]


class Documents(MenuGroup):
    icon = icons.INSERT_DRIVE_FILE_OUTLINED
    label = 'Документы'


roots = [
    Directories,
    Documents,
]
