from tortoise import Tortoise

from admin.app import CRuMbAdmin
from . import settings, menu_groups


class CakeInLawAdmin(CRuMbAdmin):
    title: str = 'CakeInLaw'
    menu_groups = [*menu_groups.roots]

    @classmethod
    async def on_startup(cls):
        await Tortoise.init(config=settings.DATABASE)
        import configuration.repositories
        import configuration.resources

    @classmethod
    async def on_shutdown(cls):
        await Tortoise.close_connections()

    # @classmethod
    # async def run_target(cls, page):
    #     page.title = cls.title
    #     page.padding = 0
    #     app = cls(page)
    #     await page.add_async(app)
    #     from admin.layout import PayloadInfo
    #     await app.open(PayloadInfo('directories.Customer', 'create'))
