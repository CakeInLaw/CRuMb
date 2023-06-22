from flet import Page, NavigationRail, NavigationRailDestination, Text
import flet as ft


__all__ = ["Sidebar"]


class Sidebar(NavigationRail):
    menu_items: list[NavigationRailDestination]
    page: Page

    def __init__(self, page: Page, **kwargs):
        kwargs.setdefault('extended', True)
        kwargs.setdefault('min_width', 50)
        kwargs.setdefault('min_extended_width', 200)
        kwargs.setdefault('label_type', 'none')

        kwargs.setdefault('destinations', [
            NavigationRailDestination(
                label_content=Text("Покупатели"),
                label="/dir/customers",
                icon=ft.icons.BOOK_OUTLINED,
                selected_icon=ft.icons.BOOK_OUTLINED
            ),
            NavigationRailDestination(
                label_content=Text("Поставщики"),
                label="/dir/providers",
                icon=ft.icons.PERSON,
                selected_icon=ft.icons.PERSON,
            ),
        ])

        super().__init__(**kwargs)
        self.page = page
        self.on_change = self.set_active_route

    async def toggle_sidebar(self, e):
        self.extended = not self.extended
        await self.update_async()

    async def set_active_route(self, e: ft.ControlEvent):
        self.page.route = self.destinations[e.control.selected_index].label
        await self.page.update_async()
