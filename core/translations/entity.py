from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from .interface import InterfaceTranslation


@dataclass
class EntityTranslation:
    name: str
    name_plural: str

    fields: dict[str, str]

    choice_template: str = '{self.name_plural}: Выбор'
    create_template: str = '{self.name}: Создание'
    edit_template: str = '{self.name}: {instance}'
    interface: InterfaceTranslation = field(init=False)

    def choice(self, **kwargs):
        return self.choice_template.format(self=self, **kwargs)

    def create(self, **kwargs):
        return self.create_template.format(self=self, **kwargs)

    def edit(self, **kwargs):
        return self.edit_template.format(self=self, **kwargs)

    def field(self, name: str) -> Optional[str]:
        return self.fields.get(name)
