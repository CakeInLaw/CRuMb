from core.users.model import BaseUser


__all__ = ["User"]


class User(BaseUser):

    class Meta:
        table = "dir__users"
