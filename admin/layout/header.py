from typing import TYPE_CHECKING

from flet import Page, AppBar, IconButton, Text, PopupMenuButton, PopupMenuItem

if TYPE_CHECKING:
    from ..app import CRuMbAdmin


__all__ = ["Header"]


class Header(AppBar):
    _toggle_nav_rail_button: IconButton
    app: "CRuMbAdmin"
    page: Page

    def __init__(self, app: "CRuMbAdmin", **kwargs):
        kwargs.setdefault('leading', None)
        kwargs.setdefault('leading_width', None)
        kwargs.setdefault('automatically_imply_leading', False)
        kwargs.setdefault('title', Text(app.title))
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
        self.app = app
