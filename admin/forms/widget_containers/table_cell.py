from admin.components.table import TableCell
from .base import W, BaseWidgetContainer


class TableCellWidgetContainer(BaseWidgetContainer[W], TableCell):
    def __init__(self, widget: W):
        BaseWidgetContainer.__init__(self, widget=widget)
        TableCell.__init__(self, content=self.widget_tooltip)
        if self.widget.editable:
            self.on_double_tap_down = self.double_click_handler
        self.widget.apply_container(self)

    async def double_click_handler(self, e):
        self.activate_row()
        await self.widget.start_change_event_handler(e)
        await self.body.update_async()

    def get_width(self):
        return self.width

    def set_error_text(self, text: str):
        super().set_error_text(text)
        self.change_bgcolor()

    def rm_error(self):
        super().rm_error()
        self.change_bgcolor()

    def change_bgcolor(self):
        if self.widget.has_error:
            self.container.bgcolor = 'error,0.2'
        else:
            super().change_bgcolor()
