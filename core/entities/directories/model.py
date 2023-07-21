from core.orm.base_model import BaseModel, RelatedListValueModel


__all__ = ["Directory", ]


class Directory(BaseModel):
    class Meta:
        abstract = True


class DirectoryListValue(RelatedListValueModel):
    class Meta:
        abstract = True
