from flet import Container

from admin.table import TableCell
from .base import W, BaseWidgetContainer


class TableCellWidgetContainer(BaseWidgetContainer[W], TableCell):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        self.container = Container(content=self.widget_tooltip)
        TableCell.__init__(self, content=self.container)
