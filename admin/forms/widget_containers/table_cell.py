from flet import Container

from admin.table import TableCell
from .base import W, BaseWidgetContainer


class TableCellWidgetContainer(BaseWidgetContainer[W], TableCell):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        self.container = Container(content=self.widget_tooltip)
        TableCell.__init__(self, content=self.container)

    def set_error_text(self, text: str):
        super().set_error_text(text)
        self.change_bgcolor()

    def rm_error(self):
        super().rm_error()
        self.change_bgcolor()

    def change_bgcolor(self):
        if self.widget.has_error:
            self.bgcolor = 'error,0.2'
        else:
            super().change_bgcolor()
