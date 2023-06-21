from tortoise import fields
from core.directories.model import Directory


__all__ = ["Provider"]


class Provider(Directory):
    id: int = fields.IntField(pk=True)
    name: str = fields.CharField(max_length=50)
    register_address: str = fields.CharField(max_length=200)

    class Meta:
        table = "dir__providers"
        ordering = ('id',)
