from typing import TYPE_CHECKING

from flet import Container, Stack, BoxShadow, ShadowBlurStyle

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin


__all__ = ["ContentBox"]


class ContentBox(Container):

    def __init__(self, app: "CRuMbAdmin"):
        super().__init__(
            expand=True,
            bgcolor='white',
            shadow=BoxShadow(
                blur_radius=15,
                offset=(0, 14),
                color='#1C1B1F,0.2'
            ),
        )
        self.app = app
        self.containers = []
        self.content = Stack(self.containers, expand=True)

    def add_container(self) -> Container:
        container = Container(expand=True)
        self.containers.append(container)
        return container

    def rm_container(self, container: Container):
        self.containers.remove(container)
