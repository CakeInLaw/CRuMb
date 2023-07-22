from dataclasses import dataclass

from flet import Container, Row, Column

from .base import ObjectInputBaseWidget, ObjectInputBase


class ObjectInputWidget(ObjectInputBaseWidget, Container):
    children_in_table_cell: bool = False

    def __init__(self, variant: str = 'row', **kwargs):
        super().__init__(**kwargs)
        self.variant = variant
        self.content = self.create_content()

    def create_content(self) -> Row | Column:
        widgets = self.get_widgets()
        match self.variant:
            case 'row':
                return Row(widgets, wrap=True)
            case 'column':
                return Column(widgets)
            case _:
                raise ValueError(f'Варианта отображения "{self.variant}" не существует')


@dataclass
class ObjectInput(ObjectInputBase[ObjectInputWidget]):
    variant: str = 'row'

    @property
    def widget_type(self):
        return ObjectInputWidget
