from dataclasses import dataclass, field
from .entity import EntityTranslation


@dataclass
class InterfaceTranslation:
    __lang__: str
    settings: str
    sign_in: str
    sign_out: str

    common_fields: dict[str, str]
    entities: dict[str, EntityTranslation] = field(default_factory=dict)

    def add_common_fields(self, **fields: str):
        self.common_fields.update(**fields)

    def add_entity(self, name: str, translation: EntityTranslation):
        self.entities[name] = translation
        translation.interface = self

    def translate(self, key: str):
        res = getattr(self, key, None)
        if res is None:
            raise KeyError(f'Нет перевода для {key}')
        return res

    def translate_field(self, entity_name: str, field_name: str):
        res = self.entities[entity_name].field(field_name)
        if res is None:
            res = self.common_fields.get(field_name)
        if res is None:
            res = field_name
        return res
