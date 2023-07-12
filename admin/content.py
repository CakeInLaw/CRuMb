from typing import TYPE_CHECKING

from flet import Page, Container, BoxShadow, ShadowBlurStyle

if TYPE_CHECKING:
    from .app import CRuMbAdmin


__all__ = ["Content"]


class Content(Container):
    app: "CRuMbAdmin"
    page: Page
    root: Container

    def __init__(self, app: "CRuMbAdmin"):
        super().__init__(
            expand=True,
            shadow=BoxShadow(
                blur_radius=15,
                blur_style=ShadowBlurStyle.OUTER,
                color='#1C1B1F,0.2'
            )
        )

        self.app = app
