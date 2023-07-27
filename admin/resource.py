import inspect
from typing import TYPE_CHECKING, Generic, Type, Callable, Coroutine, Optional, Any, TypeVar

from flet import Control, Text, icons

from core.enums import FieldTypes
from core.types import PK
from core.orm.base_model import BaseModel
from core.exceptions import ItemNotFound, ObjectErrors
from core.repository import REPOSITORY
from admin.forms import ModelInputForm, Primitive, ListForm, ChoiceForm

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.layout import BOX


__all__ = ["Resource"]

C = TypeVar('C', bound=Control)


class Resource(Generic[REPOSITORY]):
    repository: Type[REPOSITORY]
    app: "CRuMbAdmin"
    ICON = icons.SPORTS_GYMNASTICS

    list_form_primitive: Primitive = None
    choice_form_primitive: Primitive = None

    model_form: Type[ModelInputForm] = ModelInputForm
    form_primitive: Primitive = None
    create_model_form: Optional[Type[ModelInputForm]] = None
    create_form_primitive: Primitive = None
    edit_model_form: Optional[Type[ModelInputForm]] = None
    edit_form_primitive: Primitive = None

    def __init__(self, app: "CRuMbAdmin") -> None:
        self.app = app
        self.translation = self.repository.get_translation(self.app.LANG)

    def relative_resource(self, field_name: str) -> "Resource":
        return self.app.find_resource(self.repository.repository_of(field_name).entity())

    async def get_list_primitive(self):
        return self.list_form_primitive

    async def get_choice_primitive(self):
        return self.choice_form_primitive or self.list_form_primitive

    async def get_create_form_primitive(self):
        return self.create_form_primitive or self.form_primitive

    async def get_create_model_form(self):
        return self.create_model_form or self.model_form

    async def get_edit_form_primitive(self):
        return self.edit_form_primitive or self.form_primitive

    async def get_edit_model_form(self):
        return self.edit_model_form or self.model_form

    async def get_list_form(self, box: "BOX") -> ListForm:
        view = ListForm(box=box, primitive=self.list_form_primitive)
        return self.with_tab_title(view, 'list')

    async def get_choice_view(
            self,
            box: "BOX",
            make_choice: Callable[[Optional[BaseModel]], Coroutine[Any, Any, None]],
    ) -> ChoiceForm:
        view = ChoiceForm(
            box=box,
            primitive=self.choice_form_primitive or self.list_form_primitive,
            make_choice=make_choice
        )
        return self.with_tab_title(view, 'choice')

    async def get_create_form(
            self,
            box: "BOX",
            on_success: Callable[[ModelInputForm, BaseModel], Coroutine[Any, Any, None]] = None,
            on_error: Callable[[ModelInputForm, ObjectErrors], Coroutine[Any, Any, None]] = None,
    ) -> ModelInputForm:
        model_form = self.create_model_form or self.model_form
        form = model_form(
            resource=self,
            box=box,
            primitive=await self.get_create_form_primitive(),
            on_success=on_success,
            on_error=on_error,
        )
        return self.with_tab_title(form, 'create')

    async def get_edit_form(
            self,
            box: "BOX",
            pk: PK,
            on_success: Callable[[ModelInputForm, BaseModel], Coroutine[Any, Any, None]] = None,
            on_error: Callable[[ModelInputForm, ObjectErrors], Coroutine[Any, Any, None]] = None,
    ) -> ModelInputForm | Control:
        try:
            instance = await self.repository(
                by='admin',
                extra={'target': 'edit'}
            ).get_one(pk)
        except ItemNotFound:
            error = Text('Объект не найден')
            error.__tab_title__ = 'Ошибка'
            return error
        primitive = self.edit_form_primitive or self.form_primitive
        model_form = self.edit_model_form or self.model_form
        form = model_form(
            resource=self,
            box=box,
            primitive=primitive,
            instance=instance,
            on_success=on_success,
            on_error=on_error,
        )
        return self.with_tab_title(form, 'edit', instance=instance)

    @classmethod
    def entity(cls) -> str:
        return cls.repository.entity()

    @classmethod
    def default_method(cls) -> str:
        return 'list'

    def _methods(self) -> dict[str, Callable[["BOX", ...], Control | Coroutine[Any, Any, Control]]]:
        return {
            'list': self.get_list_form,
            'choice': self.get_choice_view,
            'create': self.get_create_form,
            'edit': self.get_edit_form,
        }

    @property
    def methods(self) -> dict[str, Callable[["BOX", ...], Control | Coroutine[Any, Any, Control]]]:
        if not hasattr(self, '_cached_methods'):
            setattr(self, '_cached_methods', self._methods())
        return getattr(self, '_cached_methods')

    async def get_payload(self, box: "BOX", method: str, **query) -> Control:
        callback = self.methods[method]
        if inspect.iscoroutinefunction(callback):
            payload = await callback(box, **query)
        else:
            payload = callback(box, **query)
        return payload

    # Частые переводы
    @property
    def name(self) -> str:
        return self.translation.name

    @property
    def name_plural(self) -> str:
        return self.translation.name_plural

    def translate_field(self, field_name: str) -> str:
        translation = self.translation.field(field_name)
        if translation is None:
            field_type = self.repository.get_field_type(field_name)
            if field_type in FieldTypes.single_relation():
                translation = self.relative_resource(field_name).name
            elif field_type in FieldTypes.multiple_relation():
                translation = self.relative_resource(field_name).name_plural
            else:
                translation = field_name
        return translation

    # Функции для установки названия вкладок с мультиязычность и параметрами.
    def with_tab_title(self, control: C, method: str, **kwargs) -> C:
        control.__tab_title__ = getattr(self, f'_tab_title_{method}')(**kwargs)
        return control

    def _tab_title_list(self) -> str:
        return self.name_plural

    def _tab_title_choice(self) -> str:
        return self.name_plural

    def _tab_title_create(self) -> str:
        return self.translation.create()

    def _tab_title_edit(self, instance: BaseModel) -> str:
        return self.translation.edit(instance=instance)

    # Функции для сравнения параметров вкладок.
    # Если True, то вкладка создаваться не будет и откроется существующая
    # Если False, то создастся новая вкладка
    def compare_tab(self, method: str, query1: dict[str, Any], query2: dict[str, Any]) -> bool:
        return getattr(self, f'_compare_tab_{method}')(query1, query2)

    def _compare_tab_list(self, query1: dict[str, Any], query2: dict[str, Any]) -> bool:
        return True

    def _compare_tab_choice(self, query1: dict[str, Any], query2: dict[str, Any]) -> bool:
        return False

    def _compare_tab_create(self, query1: dict[str, Any], query2: dict[str, Any]) -> bool:
        return True

    def _compare_tab_edit(self, query1: dict[str, Any], query2: dict[str, Any]) -> bool:
        return query1['pk'] == query2['pk']
