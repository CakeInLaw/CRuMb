from typing import Optional


class Fstr:
    def __init__(self, template: str):
        self.template = template

    def __get__(self, instance, owner):
        if instance is None:
            return self

        def formatter(**kwargs):
            return self.template.format(self=instance, **kwargs)

        return formatter


class Translation:
    name: str
    name_plural: str

    fields: dict[str, str]
    _common_fields: dict[str, str]

    _create: str
    create_template: str = '{self.name}: {self._create}'

    edit_template: str = '{self.name}: {instance}'

    def __init__(
            self,
            name: str,
            name_plural: str,
            fields: dict[str, str] = None,
            create: str = None,
            edit: str = None,
    ):
        self.name = name
        self.name_plural = name_plural
        self.fields = fields or {}
        if create:
            self.create_template = create
        if edit:
            self.edit_template = edit

    def create(self, **kwargs):
        return self.create_template.format(self=self, **kwargs)

    def edit(self, **kwargs):
        return self.edit_template.format(self=self, **kwargs)

    def field(self, name: str) -> Optional[str]:
        result = self.fields.get(name)
        if result is None:
            result = self._common_fields.get(name)
        return result


class TranslationRu(Translation):
    _create: str = 'Создание'
    _common_fields = {
        'name': 'Наименование',
        'ordering': '№',
    }


class TranslationEn(Translation):
    _create: str = 'New'
    _common_fields = {
        'name': 'Name',
        'ordering': '№',
    }
