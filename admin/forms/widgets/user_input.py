from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional, Any, Generic, Type, Union, Callable, Coroutine, Literal

from flet import Control
from flet_core.event_handler import EventHandler

from admin.exceptions import InputValidationError
from ..widget_containers import BaseWidgetContainer, SimpleWidgetContainer

if TYPE_CHECKING:
    from ..form import Form


T = TypeVar('T')


class UserInputWidget(Generic[T]):

    container: "BaseWidgetContainer"

    @property
    def final_value(self) -> T:
        raise NotImplementedError

    @property
    def form(self) -> Optional["Form"]:
        if isinstance(self.parent, UserInputWidget):
            return self.parent.form
        else:
            return self.parent

    @property
    def full_name(self):
        if isinstance(self.parent, UserInputWidget):
            return f'{self.parent.full_name}.{self.name}'
        return self.name

    def __init__(
            self,
            *,
            name: str,
            label: str = None,
            helper_text: str = None,
            null: bool = False,
            required: bool = False,
            read_only: bool = False,
            initial_value: T = None,
            parent: Union["Form", "UserInputWidget"] = None,
            on_value_change: Callable[["UserInputWidget"], Coroutine[Any, Any, None] | None] = None,
            width: int | float = 250,
            height: int | float = 40,
    ):
        self.name = name
        self.label_text = label
        self.helper_text = helper_text
        self.null = null
        self.required = required
        self.read_only = read_only
        self.container_width = width
        self.container_height = height
        self.initial_value = initial_value

        self.has_error = False
        self.parent = parent
        self.on_value_change = on_value_change
        self.__on_start_changing = EventHandler()
        self.__on_end_changing = EventHandler()

    def __finalize_init__(self):
        """Для вызова в последних наследниках виджетов"""
        self.set_value(self.initial_value, initial=True)
        self.set_mode('read')
        self.on_end_changing = self.handle_value_change_and_update

    def set_mode(self, v: Literal['read', 'write']):
        pass

    def apply_container(self, container: BaseWidgetContainer):
        self.container = container
        if isinstance(self.container, SimpleWidgetContainer):
            self.container.with_label = True
            self.container.with_border = True
            if self.container_width:
                self.container.set_width(self.container_width)
            if self.container_height:
                self.container.set_height(self.container_height)

    def set_value(self, value: T, initial: bool = False):
        raise NotImplementedError

    def has_changed(self) -> bool:
        return self.initial_value == self.final_value

    def _validate(self) -> None:
        pass

    def validate(self) -> None:
        try:
            self._validate()
            self._on_success_validation()
        except InputValidationError as err:
            self._on_error_validation(err)
            raise err

    def _on_success_validation(self):
        if self.has_error:
            self.rm_error()

    def _on_error_validation(self, err: InputValidationError):
        self.set_error_text(err.msg)

    def set_error_text(self, text: Optional[str]):
        self.has_error = True
        self.container.set_error_text(text)

    def rm_error(self):
        self.has_error = False
        self.container.rm_error()

    def set_error(self, err: dict[str, Any]):
        self.set_error_text(err.get('msg', 'Какая-то ошибка'))

    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except InputValidationError:
            return False

    def _transform_value(self):
        pass

    async def handle_value_change_and_update(self, widget: "UserInputWidget"):
        self.handle_value_change(widget=widget)
        await self.form.update_async()

    def handle_value_change(self, widget: "UserInputWidget"):
        if self is widget:
            self._transform_value()
            if not self.is_valid():
                return
        if self.on_value_change:
            self.on_value_change(widget)
        self.parent.handle_value_change(widget)

    @property
    def on_start_changing(self):
        return self.__on_start_changing

    @on_start_changing.setter
    def on_start_changing(self, v: Callable[["UserInputWidget"], ...]):
        if v:
            self.__on_start_changing.subscribe(v)

    async def start_change_event_handler(self, e):
        self.set_mode('write')
        await self.on_start_changing.get_handler()(self)
        await self.form.update_async()

    @property
    def on_end_changing(self):
        return self.__on_end_changing

    @on_end_changing.setter
    def on_end_changing(self, v: Callable[["UserInputWidget"], ...]):
        if v:
            self.__on_end_changing.subscribe(v)

    async def end_change_event_handler(self, e):
        self.set_mode('read')
        return await self.on_end_changing.get_handler()(self)

    async def end_change(self):
        await self.update_async()


class UndefinedValue:
    pass


_I = TypeVar('_I', bound=Union[Control, UserInputWidget])


@dataclass
class UserInput(Generic[_I]):
    name: str
    label: str = None
    helper_text: str = None
    null: bool = False
    required: bool = False
    read_only: bool = False
    on_value_change:  Callable[[UserInputWidget], Coroutine[Any, Any, None]] = None
    width: int | float = 350
    height: int | float = 40

    def widget(
            self,
            parent: Union["Form", UserInputWidget],
            initial: Any = UndefinedValue,
            **extra
    ) -> _I:
        if initial is UndefinedValue:
            initial = self.default_initial
        kwargs = {**self.__dict__, **extra}
        return self.widget_type(parent=parent, initial_value=initial, **kwargs)

    @property
    def default_initial(self) -> Any:
        return None

    @property
    def widget_type(self) -> Type[_I]:
        raise NotImplementedError

    @property
    def is_numeric(self):
        return False
