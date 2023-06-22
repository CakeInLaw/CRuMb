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

    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8000,
        route_url_strategy="hash",
    )

    asyncio.get_event_loop().run_until_complete(
        Tortoise.close_connections()
    )
