from typing import TYPE_CHECKING

from flet import Container, Icon, Text, Row, Column, ListTile

if TYPE_CHECKING:
    from ..app import CRuMbAdmin


class MenuGroup(Container):
    def __init__(
            self,
            icon: str,
            label: str,
            app: "CRuMbAdmin",
            parent: "MenuGroup" = None
    ):
        super().__init__()
        self.icon = Icon(icon)
        self.text = Text(label)
        self.app = app
        self.expanded = False
        self.parent = parent

        self.root = Row()
        self.content = Column([

        ])

    def activate(self):
        pass

    def deactivate(self):
        pass

    def minimize(self):
        pass

    def maximize(self):
        pass
