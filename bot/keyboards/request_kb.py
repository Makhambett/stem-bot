from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def new_request_kb(request_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Взять в работу", callback_data=f"take:{request_id}")
    kb.button(text="ℹ️ Подробнее", callback_data=f"info:{request_id}")
    kb.adjust(1)
    return kb.as_markup()


def in_progress_kb(request_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🎉 Успешно", callback_data=f"done:{request_id}:success")
    kb.button(text="❌ Неуспешно", callback_data=f"done:{request_id}:failed")
    kb.button(text="ℹ️ Подробнее", callback_data=f"info:{request_id}")
    kb.adjust(1)
    return kb.as_markup()