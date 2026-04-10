from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def new_request_kb(request_id: int) -> InlineKeyboardMarkup:
    """Кнопки для новой заявки (в группе)"""
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Взять в работу", callback_data=f"take:{request_id}")
    kb.button(text="ℹ️ Подробнее", callback_data=f"info:{request_id}")
    kb.adjust(1)
    return kb.as_markup()


def in_progress_kb(request_id: int) -> InlineKeyboardMarkup:
    """Кнопки для заявки в работе (в личке у менеджера)"""
    kb = InlineKeyboardBuilder()
    kb.button(text="🎉 Успешно", callback_data=f"done:{request_id}:success")
    kb.button(text="❌ Не успешно", callback_data=f"fail:{request_id}")
    kb.adjust(2)
    return kb.as_markup()


def fail_reason_kb(request_id: int) -> InlineKeyboardMarkup:
    """Выбор причины отказа"""
    kb = InlineKeyboardBuilder()
    kb.button(text="📞 Не дозвонился", callback_data=f"fail_reason:{request_id}:no_answer")
    kb.button(text="💰 Не устроила цена", callback_data=f"fail_reason:{request_id}:price")
    kb.button(text="🚫 Клиент отказался", callback_data=f"fail_reason:{request_id}:refused")
    kb.button(text="⏰ Передумал", callback_data=f"fail_reason:{request_id}:changed_mind")
    kb.button(text="✍️ Другая причина (своя)", callback_data=f"fail_reason:{request_id}:custom")
    kb.button(text="↩️ Отмена", callback_data=f"cancel_fail:{request_id}")
    kb.adjust(1)
    return kb.as_markup()