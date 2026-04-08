from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.repositories.requests import get_request
from bot.services.manager_service import manager_has_access
from bot.services.request_service import close_request, take_request
from bot.utils.formatters import format_request_card

router = Router()


@router.callback_query(F.data.startswith("take:"))
async def take_request_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    request_id = int(callback.data.split(":")[1])
    result = await take_request(request_id=request_id, manager_id=callback.from_user.id)
    if not result["ok"]:
        return await callback.answer(result["message"], show_alert=True)

    await callback.message.edit_text(
        result["text"],
        parse_mode="HTML",
        reply_markup=result["reply_markup"],
    )
    await callback.answer("Заявка взята в работу")


@router.callback_query(F.data.startswith("done:"))
async def close_request_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    _, request_id, final_status = callback.data.split(":")
    result = await close_request(
        request_id=int(request_id),
        manager_id=callback.from_user.id,
        final_status=final_status,
    )
    if not result["ok"]:
        return await callback.answer(result["message"], show_alert=True)

    await callback.message.edit_text(result["text"], parse_mode="HTML")
    await callback.answer("Статус обновлён")


@router.callback_query(F.data.startswith("info:"))
async def request_info_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    request_id = int(callback.data.split(":")[1])
    request = await get_request(request_id)
    if not request:
        return await callback.answer("Заявка не найдена.", show_alert=True)
    await callback.answer()
    await callback.message.answer(format_request_card(request), parse_mode="HTML")