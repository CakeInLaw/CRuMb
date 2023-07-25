from dataclasses import dataclass

from flet import Container, Row, Column, Control

from .base import ObjectBaseWidget, ObjectBase
from .. import UserInput
from ... import InputGroup
from ...widget_containers import SimpleWidgetContainer


class ObjectWidget(ObjectBaseWidget[SimpleWidgetContainer], Container):
    child_container = SimpleWidgetContainer

    def __init__(self, variant: str = 'row', **kwargs):
        Container.__init__(self)
        ObjectBaseWidget.__init__(self, **kwargs)
        self.variant = variant
        self.content = self.create_content()

    def get_controls(self) -> list[Control]:
        controls = []
        for f in self.fields:
            if isinstance(f, UserInput):
                controls.append(self._create_widget_in_container(f))
            else:
                controls.append(self._build_group(f))
        return controls

    def _build_group(self, group: InputGroup) -> Control:
        controls: list[Control] = []
        for subgroup_or_input in group:
            if isinstance(subgroup_or_input, InputGroup):
                controls.append(self._build_group(subgroup_or_input))
            elif isinstance(subgroup_or_input, UserInput):
                controls.append(self._create_widget_in_container(subgroup_or_input))
        return group.to_control(controls)

    def create_content(self) -> Row | Column:
        controls = self.get_controls()
        match self.variant:
            case 'row':
                return Row(controls, wrap=True)
            case 'column':
                return Column(controls)
            case _:
                raise ValueError(f'Варианта отображения "{self.variant}" не существует')


@dataclass
class Object(ObjectBase[ObjectWidget]):
    variant: str = 'row'

    @property
    def widget_type(self):
        return ObjectWidget
