from typing import TYPE_CHECKING

from flet import Container, Row, Text, PopupMenuButton, PopupMenuItem, MainAxisAlignment, padding

if TYPE_CHECKING:
    from ..app import CRuMbAdmin


__all__ = ["Header"]


class Header(Container):
    app: "CRuMbAdmin"

    def __init__(self, app: "CRuMbAdmin"):
        super().__init__(bgcolor='#575B81', padding=padding.symmetric(horizontal=10))
        self.app = app
        self.content = Row(
            height=40,
            controls=[
                Text(app.title, color='background', size=20),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text="Настройки"),
                        PopupMenuItem(),  # divider
                        PopupMenuItem(text="Выход"),
                    ],
                )
            ],
            alignment=MainAxisAlignment.SPACE_BETWEEN,
        )
