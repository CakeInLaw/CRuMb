from flet import Page, AppBar, IconButton, Text, PopupMenuButton, PopupMenuItem
import flet as ft


__all__ = ["Header"]


class Header(AppBar):
    _toggle_nav_rail_button: IconButton
    page: Page

    def __init__(self, page: Page, **kwargs):
        self.page = page
        kwargs.setdefault('leading', self.toggle_nav_rail_button)
        kwargs.setdefault('leading_width', None)
        kwargs.setdefault('automatically_imply_leading', False)
        kwargs.setdefault('title', Text('CakeInLaw'))
        kwargs.setdefault('center_title', False)
        kwargs.setdefault('toolbar_height', 40)
        kwargs.setdefault('color', 'white')
        kwargs.setdefault('bgcolor', '#575B81')
        kwargs.setdefault('elevation', None)
        kwargs.setdefault('actions', [
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="Настройки"),
                    PopupMenuItem(),  # divider
                    PopupMenuItem(text="Выход"),
                ]
            ),
        ])
        super().__init__(**kwargs)

    @property
    def toggle_nav_rail_button(self) -> IconButton:
        if not hasattr(self, '_toggle_nav_rail_button'):
            self._toggle_nav_rail_button = IconButton(
                icon=ft.icons.ARROW_CIRCLE_LEFT,
                selected=False,
                selected_icon=ft.icons.ARROW_CIRCLE_RIGHT,
                on_click=self.toggle_nav_rail
            )
        return self._toggle_nav_rail_button

    async def toggle_nav_rail(self, e):
        btn = self.toggle_nav_rail_button
        btn.selected = not btn.selected
        await self.toggle_nav_rail_button.update_async()
