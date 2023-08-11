from core.repository import register_repository
from core.translations.langs import ru, en
from core.users.repository import BaseUserRepository

from .model import User


__all__ = ["UserRepository"]


@register_repository
class UserRepository(BaseUserRepository[User]):
    model = User

    _t_ru = ru.Entity(
        name='Пользователь',
        name_plural='Пользователи',
        fields={
            'username': 'Логин',
            'is_superuser': 'Суперпользователь',
            'can_login_admin': 'Может авторизоваться в админке',
            'is_active': 'Активный',
            'created_at': 'Дата и время создания',
            'password': 'Пароль',
            're_password': 'Повторите пароль',
        },
    )

    _t_en = en.Entity(
        name='User',
        name_plural='Users',
        fields={
            'username': 'Username',
            'is_superuser': 'Is superuser',
            'can_login_admin': 'Can login admin panel',
            'is_active': 'Is active',
            'created_at': 'Created at',
            'password': 'Password',
            're_password': 'Repeat password',
        },
    )
