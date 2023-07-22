import flet as ft

from .admin import CakeInLawAdmin


class TestAdmin(CakeInLawAdmin):
    @classmethod
    def run_target(cls, page: ft.Page):
        page.title = "Tooltip Example"

        class InputContainer(ft.Container):
            def __init__(
                    self,
                    content: ft.Control,
                    label: str = None,
            ):
                super().__init__(content=content)


        page.add(
            InputContainer(ft.Dropdown(
                dense=True,
                label='Sasha',
                border=ft.InputBorder.UNDERLINE,
                border_radius=10,
                options=(
                    ft.dropdown.Option(key=1, text='Sasha'),
                    ft.dropdown.Option(key=2, text='Sasha2'),
                    ft.dropdown.Option(key=3, text='Sasha3'),
                    ft.dropdown.Option(key=4, text='Sasha4'),
                    ft.dropdown.Option(key=5, text='Sasha5'),
                )
            ))
        )


TestAdmin.run_app(
    view=ft.WEB_BROWSER,
    port=8000,
)

