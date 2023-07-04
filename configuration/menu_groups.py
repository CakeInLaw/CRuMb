from flet import icons

from admin.layout import MenuGroup


class Sells(MenuGroup):
    icon = icons.SHOPPING_CART_CHECKOUT_OUTLINED
    label = 'Продажи'


class Receives(MenuGroup):
    icon = icons.ADD_SHOPPING_CART_OUTLINED
    label = 'Покупки'


class Storage(MenuGroup):
    icon = icons.STORAGE_OUTLINED
    label = 'Склад'


class Prices(MenuGroup):
    icon = icons.PRICE_CHANGE_OUTLINED
    label = 'Цены'


roots = [
    Sells,
    Receives,
    Storage,
    Prices,
]
