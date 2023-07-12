import re
from random import choices
from string import hexdigits
from typing import Optional

from tortoise import timezone
from passlib.context import CryptContext

from core.exceptions import AnyFieldError
from core.repository import default_repository
from core.entities.directories import DirectoryRepository
from core.types import DATA, MODEL

from ..models import User


__all__ = ["UserRepository"]


PasswordIncorrect = AnyFieldError('password_incorrect', 'Некорректный пароль')
PasswordMismatch = AnyFieldError('password_mismatch', 'Пароли не совпадают')
UNUSED_PASSWORD_PREFIX = '!'


@default_repository
class UserRepository(DirectoryRepository):
    model = User

    hidden_fields: set[str] = {'password_hash', 'password_change_dt', 'password_salt'}
    extra_allowed = {'password', 're_password'}

    # обязательны 1 буква и цифра; допустимы буквы (латиница), цифры и !@#$%^&*-_=+
    password_pattern = re.compile('^(?=.*[A-Za-z])(?=.*[1-9])[A-Za-z1-9!@#$%^&*-_=+]{8,30}$')
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def _validate_password(
            self,
            value: str,
            data: DATA,
            instance: Optional[User]
    ) -> None:
        if self.password_pattern.match(value):
            raise PasswordIncorrect

    async def _validate_re_password(
            self,
            value: str,
            data: DATA,
            instance: Optional[User]
    ):
        if value != data.get('password'):
            raise PasswordMismatch

    async def handle_create(
            self,
            data: DATA,
            extra_data: DATA
    ) -> MODEL:
        data['password_change_dt'] = timezone.now()
        password = extra_data.get('password')
        if password:
            data['password_hash'] = self.create_password_hash(password)
        else:
            random_pwd = ''.join(choices(hexdigits, k=8))
            data['password_hash'] = UNUSED_PASSWORD_PREFIX + self.create_password_hash(random_pwd)
        return await super().handle_create(data, extra_data)

    @classmethod
    def create_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def password_is_unused(cls, password_hash: str) -> bool:
        return password_hash.startswith(UNUSED_PASSWORD_PREFIX)

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        if cls.password_is_unused(password):
            return False
        return cls.pwd_context.verify(password, password_hash)
