from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb(cart_count: int = 0):
    cart_label = f"🧺 Корзина ({cart_count})" if cart_count > 0 else "🧺 Корзина"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪑 Мебель",            callback_data="cat_mebel")],
        [InlineKeyboardButton(text="💡 Электротехника",    callback_data="cat_electro")],
        [InlineKeyboardButton(text="🎨 Декор",             callback_data="cat_decor")],
        [InlineKeyboardButton(text="💻 Цифровые продукты", callback_data="cat_digital")],
        [InlineKeyboardButton(text="🔬 Оборудование",      callback_data="cat_equipment")],
        [InlineKeyboardButton(text=cart_label,             callback_data="show_cart")],
        [InlineKeyboardButton(text="📞 Контакты",          callback_data="faq")],
    ])


def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ])


def manager_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика",       callback_data="manager_stats")],
        [InlineKeyboardButton(text="📋 Последние заявки", callback_data="manager_orders")],
        [InlineKeyboardButton(text="🔍 Поиск заявки",     callback_data="manager_search")],
        [InlineKeyboardButton(text="👥 Список клиентов",  callback_data="manager_clients")],
        [InlineKeyboardButton(text="🛍 Каталог",          callback_data="open_catalog")],
    ])


def reply_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🪑 Мебель"),          KeyboardButton(text="💡 Электротехника")],
            [KeyboardButton(text="🎨 Декор"),            KeyboardButton(text="💻 Цифровые продукты")],
            [KeyboardButton(text="🔬 Оборудование"),     KeyboardButton(text="🧺 Корзина")],
            [KeyboardButton(text="📞 Контакты")],
        ],
        resize_keyboard=True,
        persistent=True
    )


def manager_reply_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Статистика"),      KeyboardButton(text="📋 Последние заявки")],
            [KeyboardButton(text="🔍 Поиск заявки"),    KeyboardButton(text="👥 Список клиентов")],
            [KeyboardButton(text="🛍 Каталог")],
        ],
        resize_keyboard=True,
        persistent=True
    )
