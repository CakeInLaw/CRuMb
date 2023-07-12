from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Optional, Any, Generic, Type, Union

from flet import Control, ControlEvent

from admin.exceptions import InputValidationError

if TYPE_CHECKING:
    from ..form import Form


T = TypeVar('T')


class UserInputWidget(Generic[T]):
    can_handle_blur: bool = True

    def __init__(
            self,
            *,
            name: str = None,
            label: Optional[str] = None,
            validate_on_blur: bool = True,
            required: bool = False,
            initial_value: T = None,
            form: "Form" = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self.required = required
        self.validate_on_blur = validate_on_blur

        self.initial_value = initial_value
        self._set_initial_value(self.initial_value)

        self.form = form
        if self.can_handle_blur:
            self.on_blur = self.handle_blur

    @property
    def final_value(self) -> T:
        raise NotImplementedError

    def _set_initial_value(self, value: T) -> None:
        raise NotImplementedError

    def has_changed(self) -> bool:
        return self.initial_value == self.final_value

    def _validate(self) -> None:
        pass

    async def validate(self, reraise: bool = False) -> None:
        try:
            self._validate()
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

    async def handle_blur(self, e: ControlEvent):
        if self.validate_on_blur:
            await self.validate()


class UndefinedValue:
    pass


_I = TypeVar('_I', bound=Union[Control, UserInputWidget])


@dataclass
class UserInput(Generic[_I]):
    name: str
    label: str
    validate_on_blur: bool = True
    required: bool = False

    def widget(self, form: "Form", name_prefix: str = None, initial: Any = UndefinedValue) -> _I:
        if initial is UndefinedValue:
            initial = self.default_initial
        kwargs = {**self.__dict__}
        if name_prefix:
            kwargs['name'] = f'{name_prefix}.{kwargs["name"]}'
        return self.widget_type(**kwargs, form=form, initial_value=initial)

    @property
    def default_initial(self) -> Any:
        return None

    @property
    def widget_type(self) -> Type[_I]:
        raise NotImplementedError
