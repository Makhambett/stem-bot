import httpx
from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot.config import settings

router = Router()

STATUS_LABELS = {
    "new": "🟡 Новая",
    "in_progress": "🟠 В работе",
    "done": "✅ Закрыта",
    "rejected": "❌ Отклонена",
}


# ─── Текст сообщения о заявке ──────────────────────────────────
def app_detail_text(app: dict, manager_name: str = None) -> str:
    username_line = ""
    if app.get("username"):
        username_line = f"📱 <b>Telegram:</b> @{app['username']}\n"

    text = (
        f"📥 <b>Новая заявка с сайта</b>\n\n"
        f"🆔 <b>ID:</b> #{app['id']}\n"
        f"📦 <b>Товар:</b> {app['product_name']}\n"
        f"🔖 <b>Артикул:</b> {app.get('article') or '—'}\n"
        f"🌐 <b>Ссылка:</b> {app.get('product_url') or '—'}\n\n"
        f"👤 <b>Имя:</b> {app['name']}\n"
        f"📞 <b>Телефон:</b> {app['phone']}\n"
        f"{username_line}"
        f"💬 <b>Комментарий:</b> {app.get('comment') or '—'}\n\n"
        f"📌 <b>Статус:</b> {STATUS_LABELS.get(app['status'], app['status'])}\n"
        f"🕒 <b>Время:</b> {app['created_at']}"
    )
    if manager_name:
        text += f"\n👷 <b>Менеджер:</b> {manager_name}"
    return text


# ─── Клавиатура для новой заявки (с кнопкой Принять) ──────────
def new_app_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🟠 Принять",
                callback_data=f"take:{app_id}"
            ),
            InlineKeyboardButton(
                text="✅ Закрыть",
                callback_data=f"appstatus:done:{app_id}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"appstatus:rejected:{app_id}"
            ),
        ]
    ])


# ─── Клавиатура после взятия заявки (без кнопки Принять) ──────
def action_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Закрыть",
                callback_data=f"appstatus:done:{app_id}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить",
                callback_data=f"appstatus:rejected:{app_id}"
            ),
        ]
    ])


# ─── Отправка уведомления в группу (вызывается из FastAPI) ────
async def notify_new_application(bot: Bot, app: dict):
    """
    Вызывается из FastAPI-роутера при создании новой заявки.
    Отправляет сообщение в group_chat_id из settings.
    """
    text = app_detail_text(app)
    keyboard = new_app_keyboard(app["id"])

    await bot.send_message(
        chat_id=settings.group_chat_id,
        text=text,
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ─── Обработчик кнопки "Принять" ──────────────────────────────
@router.callback_query(F.data.startswith("take:"))
async def callback_take(callback: CallbackQuery):
    app_id = int(callback.data.split(":")[1])
    manager_id = callback.from_user.id
    manager_name = callback.from_user.full_name

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"{settings.backend_url}/api/applications/{app_id}/take",
            json={"manager_id": manager_id, "manager_name": manager_name},
        )

    if resp.status_code == 400:
        await callback.answer(
            "Эту заявку уже взял другой менеджер.",
            show_alert=True
        )
        return

    if resp.status_code != 200:
        await callback.answer("Ошибка при взятии заявки.", show_alert=True)
        return

    app = resp.json()
    await callback.answer(f"✋ Заявка #{app_id} теперь за тобой!")

    await callback.message.edit_text(
        app_detail_text(app, manager_name),
        parse_mode="HTML",
        reply_markup=action_keyboard(app_id),
    )


# ─── Обработчик кнопок "Закрыть" / "Отклонить" ────────────────
@router.callback_query(F.data.startswith("appstatus:"))
async def callback_appstatus(callback: CallbackQuery):
    parts = callback.data.split(":")
    _, new_status, app_id = parts

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.patch(
            f"{settings.backend_url}/api/applications/{app_id}/status",
            params={"status": new_status},
        )
        resp.raise_for_status()

    label = STATUS_LABELS.get(new_status, new_status)
    await callback.answer(f"Статус обновлён: {label}", show_alert=False)

    try:
        lines = []
        for line in (callback.message.text or "").split("\n"):
            if "Статус:" in line:
                lines.append(f"📌 <b>Статус:</b> {label}")
            else:
                lines.append(line)
        await callback.message.edit_text(
            "\n".join(lines),
            parse_mode="HTML",
            reply_markup=None,
        )
    except Exception:
        pass


# ─── Команда /my_queue ─────────────────────────────────────────
@router.message(Command("my_queue"))
async def cmd_my_queue(message: Message):
    manager_id = message.from_user.id

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            f"{settings.backend_url}/api/applications/manager/{manager_id}"
        )
        if resp.status_code != 200:
            await message.answer("Ошибка получения заявок.")
            return
        apps = resp.json()

    if not apps:
        await message.answer("У вас пока нет заявок.")
        return

    active = [a for a in apps if a["status"] == "in_progress"]
    done = [a for a in apps if a["status"] == "done"]
    rejected = [a for a in apps if a["status"] == "rejected"]

    text = (
        f"📊 <b>Ваша статистика:</b>\n\n"
        f"🟠 В работе: <b>{len(active)}</b>\n"
        f"✅ Закрыто: <b>{len(done)}</b>\n"
        f"❌ Отклонено: <b>{len(rejected)}</b>\n"
    )

    if active:
        text += "\n<b>🟠 Активные заявки:</b>\n"
        for a in active:
            text += f"  • #{a['id']} — {a['product_name']} — {a['name']} — {a['phone']}\n"

    await message.answer(text, parse_mode="HTML")