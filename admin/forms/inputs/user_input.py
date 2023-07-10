from dataclasses import dataclass
from typing import TypeVar, Optional, Any, Generic, Type, Union

from flet import Control, ControlEvent

from admin.exceptions import InputValidationError


T = TypeVar('T')
_I = TypeVar('_I', bound=Union[Control, "InputWidget"])


class UserInputWidget(Generic[T]):
    validate_on_blur: bool
    required: bool
    empty_as_none: bool

    def __init__(
            self,
            *,
            name: str = None,
            label: Optional[str] = None,
            validate_on_blur: bool = True,
            required: bool = False,
            initial_value: T = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self.required = required
        self.validate_on_blur = validate_on_blur
        if self.validate_on_blur:
            self.on_blur = self.validate

        self.initial_value = initial_value
        self._set_initial_value(self.initial_value)

    @property
    def final_value(self) -> T:
        raise NotImplementedError

    def _set_initial_value(self, value: T) -> None:
        raise NotImplementedError

    def has_changed(self) -> bool:
        return self.initial_value == self.final_value

    def _validate(self, v: Any) -> None:
        pass

    async def validate(self, e: ControlEvent = None, reraise: bool = False) -> None:
        try:
            self._validate(self.value)
            await self.on_success_validation()
        except InputValidationError as err:
            await self.on_error_validation(err)
            if reraise:
                raise err

    async def on_success_validation(self):
        pass

    async def on_error_validation(self, err: InputValidationError):
        await self.set_error_text(err.msg)

    async def set_error_text(self, text: Optional[str]):
        pass

    async def set_object_error(self, err: dict[str, Any]):
        await self.set_error_text(err.get('msg', 'Какая-то ошибка'))

    async def is_valid(self) -> bool:
        try:
            await self.validate(reraise=True)
        except InputValidationError:
            return False
        return True


class UndefinedValue:
    pass


@dataclass
class UserInput(Generic[_I]):
    name: str
    label: str
    validate_on_blur: bool = True
    required: bool = False

    def widget(self, initial: Any = UndefinedValue) -> _I:
        if initial is UndefinedValue:
            initial = self.default_initial
        return self.widget_type(**self.__dict__, initial_value=initial)

    @property
    def default_initial(self) -> Any:
        return None

    @property
    def widget_type(self) -> Type[_I]:
        raise NotImplementedError
