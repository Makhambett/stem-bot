from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.repositories.requests import get_request
from bot.services.manager_service import manager_has_access
from bot.services.request_service import close_request, take_request
from bot.utils.formatters import format_request_card
from bot.keyboards.request_kb import in_progress_kb, fail_reason_kb
from bot.repositories.managers import get_manager_current_request
from bot.states import FailReasonState


router = Router()


# ==========================================
# 🔘 КНОПКА "ВЗЯТЬ В РАБОТУ"
# ==========================================
@router.callback_query(F.data.startswith("take:"))
async def take_request_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    request_id = int(callback.data.split(":")[1])
    result = await take_request(request_id=request_id, manager_id=callback.from_user.id)
    
    if not result["ok"]:
        return await callback.answer(result["message"], show_alert=True)

    await callback.message.edit_text(
        f"✅ <b>Заявка #{request_id} взята в работу</b>\n"
        f"👤 Менеджер: {callback.from_user.full_name}",
        parse_mode="HTML",
        reply_markup=None
    )
    
    try:
        await callback.message.bot.send_message(
            chat_id=callback.from_user.id,
            text=result["text"],
            parse_mode="HTML",
            reply_markup=result["reply_markup"]
        )
        await callback.answer("✅ Заявка взята! Проверьте личные сообщения.")
    except Exception as e:
        print(f"⚠️ Не удалось отправить в личку: {e}")
        await callback.answer("⚠️ Заявка взята! Используйте /active для управления")


# ==========================================
# 🔘 КНОПКА "УСПЕШНО"
# ==========================================
@router.callback_query(F.data.startswith("done:") & F.data.endswith(":success"))
async def success_request_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    parts = callback.data.split(":")
    request_id = int(parts[1])

    result = await close_request(
        request_id=request_id,
        manager_id=callback.from_user.id,
        final_status="success",
        result_comment=None,
    )
    
    if not result["ok"]:
        return await callback.answer(result["message"], show_alert=True)

    await callback.message.edit_text(
        result["text"] + "\n\n✅ <b>Статус: Успешно завершена</b>",
        parse_mode="HTML",
        reply_markup=None
    )
    
    await callback.answer("🎉 Заявка успешно завершена!")


# ==========================================
# 🔘 КНОПКА "НЕ УСПЕШНО" → показываем причины
# ==========================================
@router.callback_query(F.data.startswith("fail:"))
async def fail_request_handler(callback: CallbackQuery):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    request_id = int(callback.data.split(":")[1])
    
    await callback.message.edit_text(
        callback.message.text,
        parse_mode="HTML",
        reply_markup=fail_reason_kb(request_id)
    )
    await callback.answer("Выберите причину отказа:")


# ==========================================
# 🔘 ВЫБОР ПРИЧИНЫ ОТКАЗА
# ==========================================
@router.callback_query(F.data.startswith("fail_reason:"))
async def fail_reason_handler(callback: CallbackQuery, state: FSMContext):
    if not await manager_has_access(callback.from_user.id):
        return await callback.answer("Нет доступа.", show_alert=True)

    parts = callback.data.split(":")
    request_id = int(parts[1])
    reason_code = parts[2]

    # Словарь причин
    reasons = {
        "no_answer": "📞 Не дозвонился",
        "price": "💰 Не устроила цена",
        "refused": "🚫 Клиент отказался",
        "changed_mind": "⏰ Передумал",
    }

    if reason_code == "custom":
        # Запрашиваем свою причину
        await state.update_data(request_id=request_id)
        await state.set_state(FailReasonState.waiting_for_custom_reason)
        await callback.message.answer(
            "✍️ <b>Введите причину отказа:</b>\n"
            "(Например: не тот товар, дорого, нашел дешевле и т.д.)\n"
            "Или нажмите /cancel для отмены",
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # Стандартная причина
    reason_text = reasons.get(reason_code, reason_code)
    
    result = await close_request(
        request_id=request_id,
        manager_id=callback.from_user.id,
        final_status="failed",
        result_comment=reason_text,
    )
    
    if not result["ok"]:
        return await callback.answer(result["message"], show_alert=True)

    await callback.message.edit_text(
        result["text"] + f"\n\n❌ <b>Причина:</b> {reason_text}",
        parse_mode="HTML",
        reply_markup=None
    )
    
    await state.clear()
    await callback.answer(f"❌ Заявка закрыта: {reason_text}")


# ==========================================
# ✍️ СВОЯ ПРИЧИНА (текст от менеджера)
# ==========================================
@router.message(FailReasonState.waiting_for_custom_reason)
async def custom_reason_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    
    custom_reason = message.text.strip()
    
    result = await close_request(
        request_id=request_id,
        manager_id=message.from_user.id,
        final_status="failed",
        result_comment=f"✍️ {custom_reason}",
    )
    
    if not result["ok"]:
        await message.answer(f"❌ Ошибка: {result['message']}")
        await state.clear()
        return

    await message.answer(
        result["text"] + f"\n\n❌ <b>Причина:</b> {custom_reason}",
        parse_mode="HTML"
    )
    
    await state.clear()
    await message.answer("✅ Заявка закрыта")


# ==========================================
# ↩️ ОТМЕНА ВЫБОРА ПРИЧИНЫ
# ==========================================
@router.callback_query(F.data.startswith("cancel_fail:"))
async def cancel_fail_handler(callback: CallbackQuery, state: FSMContext):
    request_id = int(callback.data.split(":")[1])
    request = await get_request(request_id)
    
    if not request:
        return await callback.answer("❌ Заявка не найдена", show_alert=True)
    
    manager_name = callback.from_user.full_name
    text = format_request_card(request, manager_name=manager_name)
    keyboard = in_progress_kb(request_id)
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    await state.clear()
    await callback.answer("↩️ Отменено")


# ==========================================
# 📋 КОМАНДА /active
# ==========================================
@router.message(Command("active", "my_current"))
async def cmd_active_request(message: Message):
    if not await manager_has_access(message.from_user.id):
        return await message.answer("🚫 Нет доступа.")

    current = await get_manager_current_request(message.from_user.id)
    
    if not current:
        return await message.answer("🟢 У вас нет активных заявок.")
    
    request = await get_request(current["id"])
    if not request:
        return await message.answer("❌ Ошибка: заявка не найдена.")
    
    manager_name = message.from_user.full_name
    text = format_request_card(request, manager_name=manager_name)
    keyboard = in_progress_kb(request["id"])
    
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)