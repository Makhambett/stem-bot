from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Менеджеры", callback_data="admin:managers")
    kb.button(text="📊 Статистика", callback_data="admin:stats")
    kb.adjust(1)
    return kb.as_markup()