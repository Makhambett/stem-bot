from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def mebel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛋 Диваны",    callback_data="item_divany")],
        [InlineKeyboardButton(text="🪑 Кресла",    callback_data="item_kreslo")],
        [InlineKeyboardButton(text="📦 Пуфы",      callback_data="item_pufy")],
        [InlineKeyboardButton(text="📚 Стеллажи",  callback_data="item_stellazhi")],
        [InlineKeyboardButton(text="🗄 Тумбы",     callback_data="item_tumby")],
        [InlineKeyboardButton(text="🪑 Стулья",    callback_data="item_stulya")],
        [InlineKeyboardButton(text="🚪 Шкафы",     callback_data="item_shkafy")],
        [InlineKeyboardButton(text="🍳 Кухня",     callback_data="item_kuhnya")],
        [InlineKeyboardButton(text="🪵 Столы",     callback_data="item_stoly")],
        [InlineKeyboardButton(text="⬅️ Назад",     callback_data="main_menu")],
    ])

def decor_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛 ГОС символика",  callback_data="item_gos")],
        [InlineKeyboardButton(text="🧱 3D панели",      callback_data="item_3dpanels")],
        [InlineKeyboardButton(text="💡 Освещение",      callback_data="item_lighting")],
        [InlineKeyboardButton(text="🪟 Перегородки",    callback_data="item_peregorodki")],
        [InlineKeyboardButton(text="🪴 Растения",       callback_data="item_rasteniya")],
        [InlineKeyboardButton(text="🎭 Шторы",          callback_data="item_shtory")],
        [InlineKeyboardButton(text="📋 Доски",          callback_data="item_doski")],
        [InlineKeyboardButton(text="⬅️ Назад",          callback_data="main_menu")],
    ])

def electro_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📺 Интерактивные панели", callback_data="item_interactive")],
        [InlineKeyboardButton(text="💻 Компьютеры",           callback_data="item_computers")],
        [InlineKeyboardButton(text="🖥 Инфо киоск",           callback_data="item_infokiosk")],
        [InlineKeyboardButton(text="⚙️ Станки",               callback_data="item_stanki")],
        [InlineKeyboardButton(text="🏠 Бытовая техника",      callback_data="item_bytovaya")],
        [InlineKeyboardButton(text="🖨 3Д принтеры",          callback_data="item_printers3d")],
        [InlineKeyboardButton(text="⬅️ Назад",                callback_data="main_menu")],
    ])

def order_kb(category: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Оставить заявку", callback_data=f"order_{category}")],
        [InlineKeyboardButton(text="⬅️ Назад в меню",   callback_data="main_menu")],
    ])
