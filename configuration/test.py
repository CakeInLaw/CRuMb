from .admin import CakeInLawAdmin

import flet as ft

from configuration.admin import CakeInLawAdmin


class TestAdmin(CakeInLawAdmin):
    @classmethod
    def run_target(cls, page: ft.Page):
        pass


TestAdmin.run_app(
    view=ft.WEB_BROWSER,
    port=8000,
    route_url_strategy="hash",
)

