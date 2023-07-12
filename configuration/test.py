import flet as ft

from .admin import CakeInLawAdmin


class TestAdmin(CakeInLawAdmin):
    @classmethod
    def run_target(cls, page: ft.Page):

        page.title = "AlertDialog examples"

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!"),
        )

        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete all those files?"),
            actions=[
                ft.TextButton("Yes", on_click=close_dlg),
                ft.TextButton("No", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg(e):
            page.dialog = dlg
            dlg.open = True
            page.update()

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        page.add(
            ft.ElevatedButton("Open dialog", on_click=open_dlg),
            ft.ElevatedButton("Open modal dialog", on_click=open_dlg_modal),
        )


TestAdmin.run_app(
    view=ft.WEB_BROWSER,
    port=8000,
)

