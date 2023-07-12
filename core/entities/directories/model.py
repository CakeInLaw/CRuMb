from core.orm.base_model import BaseModel


__all__ = ["Directory"]


class Directory(BaseModel):
    class Meta:
        abstract = True
