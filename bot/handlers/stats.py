from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.services.manager_service import manager_has_access
from bot.repositories.managers import (
    get_manager_current_request,
    get_manager_history,
    get_manager,
    get_manager_stats
)
from bot.utils.formatters import format_manager_personal_card, format_stats
from bot.keyboards.manager_kb import manager_panel_kb

router = Router()


# 👤 /stats_me → Личная статистика менеджера
@router.message(Command("stats_me"))
async def cmd_personal_stats(message: Message):
    if not await manager_has_access(message.from_user.id):
        return await message.answer("🚫 Нет доступа к статистике.")
    
    stats = await get_manager_stats(message.from_user.id)
    await message.answer(format_stats(stats), parse_mode="HTML")


# 📋 /my_requests → Список текущих и закрытых заявок
@router.message(Command("my_requests"))
async def cmd_my_requests(message: Message):
    if not await manager_has_access(message.from_user.id):
        return await message.answer("🚫 Нет доступа к заявкам.")

    current = await get_manager_current_request(message.from_user.id)
    history = await get_manager_history(message.from_user.id, limit=5)
    manager = await get_manager(message.from_user.id)
    name = manager["name"] if manager else "Менеджер"

    await message.answer(
        format_manager_personal_card(name, current, history),
        parse_mode="HTML",
        reply_markup=manager_panel_kb()
    )


# 🔘 Inline-кнопка "Мои заявки" (дублирует /my_requests)
@router.callback_query(F.data == "manager:my_stats")
async def callback_my_requests(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    current = await get_manager_current_request(callback.from_user.id)
    history = await get_manager_history(callback.from_user.id, limit=5)
    manager = await get_manager(callback.from_user.id)
    name = manager["name"] if manager else "Менеджер"

    await callback.message.answer(
        format_manager_personal_card(name, current, history),
        parse_mode="HTML"
    )
    await callback.answer()