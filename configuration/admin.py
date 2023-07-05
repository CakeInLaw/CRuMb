from tortoise import Tortoise

from admin.app import CRuMbAdmin
from . import settings, menu_groups


class CakeInLawAdmin(CRuMbAdmin):
    title: str = 'CakeInLaw'
    menu_groups = [*menu_groups.roots]

    @classmethod
    async def on_startup(cls):
        await Tortoise.init(config=settings.DATABASE)
        import configuration.directories.repositories
        import configuration.directories.resources

    @classmethod
    async def on_shutdown(cls):
        await Tortoise.close_connections()
