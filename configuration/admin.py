from core.admin.app import CRuMbAdmin
from . import menu_groups


class CakeInLawAdmin(CRuMbAdmin):
    title: str = 'CakeInLaw'
    menu_groups = [*menu_groups.roots]

    # @classmethod
    # async def run_target(cls, page):
    #     page.title = cls.title
    #     page.padding = 0
    #     app = cls(page)
    #     await page.add_async(app)
    #     from admin.layout import PayloadInfo
    #     await app.open(PayloadInfo('directories.Customer', 'create'))
