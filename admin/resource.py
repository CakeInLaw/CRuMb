import inspect
from typing import TYPE_CHECKING, Generic, Type, Callable, Coroutine, Optional, Any, TypeVar

from flet import Control, Text, icons

from core.enums import FieldTypes
from core.types import PK
from core.orm.base_model import BaseModel
from core.exceptions import ItemNotFound
from core.repository import REPOSITORY
from admin.list import ListView, ChoiceView
from admin.forms import Form, ModelForm, Primitive

if TYPE_CHECKING:
    from admin.app import CRuMbAdmin
    from admin.layout import BOX


__all__ = ["Resource"]

C = TypeVar('C', bound=Control)


class Resource(Generic[REPOSITORY]):
    repository: Type[REPOSITORY]
    app: "CRuMbAdmin"
    ICON = icons.SPORTS_GYMNASTICS

    datagrid_columns: list[str]
    form_primitive: Primitive = None
    create_form_primitive: Primitive = None
    edit_form_primitive: Primitive = None

    def __init__(self, app: "CRuMbAdmin") -> None:
        self.app = app
        self.translation = self.repository.get_translation(self.app.LANG)

    def relative_resource(self, field_name: str) -> "Resource":
        return self.app.find_resource(self.repository.repository_of(field_name).entity())

    async def get_list_view(self, box: "BOX") -> ListView:
        view = ListView(resource=self, box=box)
        await view.prepare()
        return self.with_tab_title(view, 'list')

    async def get_choice_view(
            self,
            box: "BOX",
            current_chosen: Optional[BaseModel],
            handle_confirm: Callable[[Optional[BaseModel]], Coroutine[Any, Any, None]],
            handle_cancel: Callable[[], Coroutine[Any, Any, None]]
    ) -> ChoiceView:
        view = ChoiceView(
            resource=self,
            box=box,
            current_chosen=current_chosen,
            handle_confirm=handle_confirm,
            handle_cancel=handle_cancel,
        )
        await view.prepare()
        return self.with_tab_title(view, 'choice')

    def _get_form(self, *, box: "BOX", obj: BaseModel = None, primitive: Primitive = None) -> Form:
        return ModelForm(
            resource=self,
            box=box,
            primitive=primitive,
            instance=obj
        )

    async def get_create_form(self, box: "BOX") -> Form | Control:
        primitive = self.create_form_primitive or self.form_primitive
        return self.with_tab_title(self._get_form(box=box, primitive=primitive), 'create')

    async def get_edit_form(self, box: "BOX", pk: PK) -> Form | Control:
        try:
            obj = await self.repository(
                by='admin',
                extra={'target': 'edit'}
            ).get_one(pk)
        except ItemNotFound:
            error = Text('Объект не найден')
            error.__tab_title__ = 'Ошибка'
            return error
        primitive = self.edit_form_primitive or self.form_primitive
        return self.with_tab_title(self._get_form(box=box, obj=obj, primitive=primitive), 'edit', obj=obj)

    @classmethod
    def entity(cls) -> str:
        return cls.repository.entity()

    @classmethod
    def default_method(cls) -> str:
        return 'list'

    def _methods(self) -> dict[str, Callable[["BOX", ...], Control | Coroutine[Any, Any, Control]]]:
        return {
            'list': self.get_list_view,
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

    def _tab_title_edit(self, obj: BaseModel) -> str:
        return self.translation.edit(obj=obj)

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
