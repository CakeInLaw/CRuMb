from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional, Any, Generic, Type, Union, Callable, Coroutine

from flet import Control, ControlEvent

from admin.exceptions import InputValidationError

if TYPE_CHECKING:
    from ..form import Form


T = TypeVar('T')


class UserInputWidget(Generic[T]):
    can_be_placed_in_table_cell: bool = True

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
            initial_value: T = None,
            in_table_cell: bool = False,
            parent: Union["Form", "UserInputWidget"] = None,
            on_value_change: Callable[["UserInputWidget"], Coroutine[Any, Any, None] | None] = None,
            default_width: int | float = 250,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.label_text = label
        self.helper_text = helper_text
        self.null = null
        self.required = required
        self.default_width = default_width
        self._set_initial_value(initial_value)

        if in_table_cell and not self.can_be_placed_in_table_cell:
            raise ValueError('Так нельзя:(')
        self.in_table_cell = in_table_cell
        self.parent = parent
        self.on_value_change = on_value_change

    def _set_initial_value(self, initial_value: T) -> None:
        self.initial_value = initial_value
        self.set_value(self.initial_value, initial=True)

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
        self.set_error_text(None)

    def _on_error_validation(self, err: InputValidationError):
        self.set_error_text(err.msg)

    def set_error_text(self, text: Optional[str]):
        pass

    def set_object_error(self, err: dict[str, Any]):
        self.set_error_text(err.get('msg', 'Какая-то ошибка'))

    def is_valid(self) -> bool:
        valid = True
        try:
            self.validate()
        except InputValidationError:
            valid = False
        return valid

    def _transform_value(self):
        pass

    def apply_in_table_cell_params(self):
        pass

    async def handle_value_change_and_update(self, event_or_control: ControlEvent | Control):
        self.handle_value_change(event_or_control=event_or_control)
        await self.form.update_async()

    def handle_value_change(self, event_or_control: ControlEvent | Control):
        control = event_or_control if isinstance(event_or_control, Control) else event_or_control.control
        if self is control:
            if not self.is_valid():
                return
            self._transform_value()
        if self.on_value_change:
            self.on_value_change(control)
        self.parent.handle_value_change(control)


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
    on_value_change:  Callable[[UserInputWidget], Coroutine[Any, Any, None]] = None
    default_width: int | float = 250

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
