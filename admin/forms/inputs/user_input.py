import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional, Any, Generic, Type, Union, Callable, Coroutine

from flet import Control, ControlEvent

from admin.exceptions import InputValidationError

if TYPE_CHECKING:
    from ..form import Form


T = TypeVar('T')


class UserInputWidget(Generic[T]):

    @property
    def final_value(self) -> T:
        raise NotImplementedError

    @property
    def form(self) -> Optional["Form"]:
        if isinstance(self.parent, UserInputWidget):
            return self.parent.form
        else:
            return self.parent

    def __init__(
            self,
            *,
            name: str,
            full_name: str = None,
            label: str = None,
            required: bool = False,
            initial_value: T = None,
            parent: Union["Form", "UserInputWidget"] = None,
            on_value_change: Callable[["UserInputWidget"], Coroutine[Any, Any, None] | None] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.full_name = full_name or name
        self.label = label or name
        self.required = required

        self.initial_value = initial_value
        self._set_initial_value(self.initial_value)

        self.parent = parent
        self.on_value_change = on_value_change

    def _set_initial_value(self, value: T) -> None:
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
        pass

    def _on_error_validation(self, err: InputValidationError):
        self.set_error_text(err.msg)

    def set_error_text(self, text: Optional[str]):
        pass

    def set_object_error(self, err: dict[str, Any]):
        self.set_error_text(err.get('msg', 'Какая-то ошибка'))

    def is_valid(self) -> bool:
        try:
            self.validate()
        except InputValidationError:
            return False
        return True

    def _transform_value(self):
        pass

    async def handle_value_change(self, event_or_control: ControlEvent | Control):
        control = event_or_control if isinstance(event_or_control, Control) else event_or_control.control
        if self is control:
            if not self.is_valid():
                return
            self._transform_value()
        if self.on_value_change:
            if asyncio.iscoroutinefunction(self.on_value_change):
                await self.on_value_change(control)
            else:
                self.on_value_change(control)
        await self.parent.handle_value_change(control)


class UndefinedValue:
    pass


_I = TypeVar('_I', bound=Union[Control, UserInputWidget])


@dataclass
class UserInput(Generic[_I]):
    name: str
    label: str
    required: bool = False
    on_value_change:  Callable[[UserInputWidget], Coroutine[Any, Any, None]] = None

    def widget(
            self,
            parent: Union["Form", UserInputWidget],
            initial: Any = UndefinedValue
    ) -> _I:
        if initial is UndefinedValue:
            initial = self.default_initial
        kwargs = {**self.__dict__}
        if isinstance(parent, UserInputWidget):
            kwargs['full_name'] = f'{parent.full_name}.{kwargs["name"]}'
        return self.widget_type(parent=parent, initial_value=initial, **kwargs)

    @property
    def default_initial(self) -> Any:
        return None

    @property
    def widget_type(self) -> Type[_I]:
        raise NotImplementedError
