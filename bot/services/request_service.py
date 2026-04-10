from bot.keyboards.request_kb import in_progress_kb
from bot.repositories.events import add_event
from bot.repositories.managers import get_manager, set_manager_busy
from bot.repositories.requests import (
    close_request_atomic,
    create_request as repo_create_request,
    get_request,
    take_request_atomic,
)
from bot.utils.formatters import format_request_card


async def create_request(client_name: str, client_phone: str, client_message: str):
    request = await repo_create_request(client_name, client_phone, client_message)
    await add_event(request["id"], 0, "created", None, "new", None)
    return request


async def take_request(request_id: int, manager_id: int):
    current = await get_request(request_id)
    if not current:
        return {"ok": False, "message": "Заявка не найдена."}

    request = await take_request_atomic(request_id, manager_id)
    if not request:
        return {"ok": False, "message": "Заявка уже взята другим менеджером."}

    # 🟢 Помечаем менеджера как занятого
    await set_manager_busy(manager_id, True)

    manager = await get_manager(manager_id)
    manager_name = manager["name"] if manager else str(manager_id)
    
    # Добавляем событие о взятии заявки
    await add_event(request_id, manager_id, "taken", current["status"], "in_progress", None)

    return {
        "ok": True,
        "text": format_request_card(request, manager_name=manager_name),
        "reply_markup": in_progress_kb(request_id),
    }


async def close_request(request_id: int, manager_id: int, final_status: str, result_comment: str | None = None):
    if final_status not in {"success", "failed"}:
        return {"ok": False, "message": "Некорректный финальный статус."}

    current = await get_request(request_id)
    if not current:
        return {"ok": False, "message": "Заявка не найдена."}
    if current["manager_telegram_id"] != manager_id:
        return {"ok": False, "message": "Только назначенный менеджер может завершить заявку."}

    request = await close_request_atomic(request_id, manager_id, final_status, result_comment)
    if not request:
        return {"ok": False, "message": "Не удалось завершить заявку."}

    manager = await get_manager(manager_id)
    manager_name = manager["name"] if manager else str(manager_id)
    await add_event(request_id, manager_id, "closed", current["status"], final_status, result_comment)

    return {
        "ok": True,
        "text": format_request_card(request, manager_name=manager_name),
        "reply_markup": None,
    }