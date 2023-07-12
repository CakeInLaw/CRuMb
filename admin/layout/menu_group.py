from typing import TYPE_CHECKING, Type, Optional
from math import pi

from flet import ListTile, Icon, Text, Column, Container, padding, icons, Rotate, Scale

from .menu_item import MenuItem, MenuItemInfo

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin


class MenuGroup(Column):
    icon: str
    label: str
    items_info: list[MenuItemInfo] = ()
    subgroups: Optional[tuple[Type["MenuGroup"]]] = ()

    def __init__(
            self,
            app: "CRuMbAdmin",
            parent: "MenuGroup" = None,
    ):
        super().__init__(spacing=0)
        self.app = app
        self.parent = parent

        self.chevron = Icon(icons.CHEVRON_RIGHT, size=20, rotate=Rotate(0), animate_rotation=100)
        self.root = ListTile(
            leading=Icon(self.icon, size=24),
            title=Text(self.label, no_wrap=True, size=14),
            trailing=self.chevron,
            dense=True,
            on_click=self.handle_click,
        )

        self.children = []
        for group_cls in self.subgroups:
            group = group_cls(app=self.app, parent=self)
            if group.children:
                self.children.append(group)
        for item_info in self.items_info:
            resource = self.app.find_resource(item_info.entity)
            self.children.append(MenuItem(
                icon=resource.ICON,
                label=resource.name,
                entity=resource.entity(),
                method=item_info.method,
                query=item_info.query,
                app=self.app,
                parent=self
            ))

        self.children_container = Container(
            Column(self.children, spacing=0),
            padding=padding.only(left=16),
            animate=100
        )

        self.controls = [
            self.root,
            self.children_container
        ]

        self.extended = False

    async def handle_click(self, e):
        self.extended = not self.extended
        await self.update_async()

    @classmethod
    def add_item_info(cls, info: MenuItemInfo):
        if isinstance(cls.items_info, tuple):
            cls.items_info = []
        cls.items_info.append(info)

    @property
    def extended(self) -> bool:
        return self._extended

    @extended.setter
    def extended(self, v: bool):
        self._extended = v
        if v:
            self.children_container.visible = True
            self.chevron.rotate.angle = pi / 2
        else:
            self.children_container.visible = False
            self.chevron.rotate.angle = 0

    def minimize(self):
        self.root.title.visible = False
        self.children_container.padding.left = 4
        self.root.trailing.visible = False
        for child in self.children:
            child.minimize()

    def maximize(self):
        self.root.title.visible = True
        self.children_container.padding.left = 16
        self.root.trailing.visible = True
        for child in self.children:
            child.maximize()
