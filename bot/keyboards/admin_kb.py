from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_main_kb() -> InlineKeyboardMarkup:
    """Основная клавиатура админа (для совместимости)"""
    kb = InlineKeyboardBuilder()
    kb.button(text="👥 Статус команды", callback_data="admin:team_status")
    kb.adjust(1)
    return kb.as_markup()


def admin_panel_kb() -> InlineKeyboardMarkup:
    """Альтернативное название (для новых вызовов)"""
    return admin_main_kb()