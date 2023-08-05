from typing import TypeVar

from core.repository import Repository, ValuesListRepository
from core.entities.directories import Directory, DirectoryListValue


__all__ = ["DirectoryRepository"]


DirectoryModel = TypeVar('DirectoryModel', bound=Directory)
DirectoryListValueModel = TypeVar('DirectoryListValueModel', bound=DirectoryListValue)


class DirectoryRepository(Repository[DirectoryModel]):
    pass
