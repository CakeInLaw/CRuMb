import json

from flet import Text

from core.exceptions import ObjectErrors
from core.admin.components.errors.base import ErrorContainer


class ObjectErrorsContainer(ErrorContainer[ObjectErrors]):
    default_title = 'Ошибка валидации'

    def get_error_text(self) -> Text:
        return Text(json.dumps(self.error.to_error(), ensure_ascii=False, indent=4))
