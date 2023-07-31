from typing import TYPE_CHECKING

from .entity import EntityTranslation
from .interface import InterfaceTranslation

if TYPE_CHECKING:
    from ..repository import Repository


class Translation:

    def __init__(
            self,
            default: str = 'ru',
            **languages: InterfaceTranslation
    ):
        self.default = default
        self.languages = languages

    def add_repository(self, repo: Repository):
        repo_languages = {}
        for lang in self.languages:
            repo_lang: EntityTranslation = getattr(repo, f'_t_{lang}', None)
            if repo_lang is None:
                ValueError(f'{repo} не имеет перевода для языка {lang}')
        for lang_name, translation in repo_languages.items():
            self.languages[lang_name].add_entity(repo.entity(), translation)

    def get(self, lang: str) -> InterfaceTranslation:
        return self.languages[lang]
