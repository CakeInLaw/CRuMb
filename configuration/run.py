import flet as ft

from configuration.admin import CakeInLawAdmin


CakeInLawAdmin.run_app(
    view=ft.WEB_BROWSER,
    port=8000,
)
