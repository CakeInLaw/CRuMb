import asyncio

import flet as ft
from tortoise import Tortoise

from configuration import settings
from .app import CRuMbAdmin


async def main(page: ft.Page):
    page.title = "CakeInLaw CRuMb"
    page.padding = 0
    app = CRuMbAdmin(page)
    await page.add_async(app)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        Tortoise.init(config=settings.DATABASE)
    )
    ##
    from core.repository import Repository, default_repository
    from configuration.directories.models import CustomerLocation, Customer, PriceGroup

    @default_repository
    class CustomerLocationRepository(Repository):
        model = CustomerLocation

    @default_repository
    class CustomerRepository(Repository):
        model = Customer

    @default_repository
    class PriceGroupRepository(Repository):
        model = PriceGroup

    async def create():
        CustomerLocationRepository().create({'order': 1, 'user_id': 1, 'delivery_address': 'URepository'})

    asyncio.get_event_loop().run_until_complete(
        CustomerLocationRepository().create({'order': 1, 'user_id': 1, 'delivery_address': 'URepository'})
    )
    ##
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8000,
        route_url_strategy="hash",
    )

    asyncio.get_event_loop().run_until_complete(
        Tortoise.close_connections()
    )
