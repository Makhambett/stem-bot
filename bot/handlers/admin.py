from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.manager_service import is_admin, list_managers
from bot.services.stats_service import get_all_stats
from bot.utils.formatters import format_stats

router = Router()


@router.message(Command("admin_panel"))
async def cmd_admin_panel(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    await message.answer(
        "Админ-панель:\n"
        "/managers - список менеджеров\n"
        "/stats - общая статистика\n"
        "/register_manager <id> - добавить менеджера\n"
        "/remove_manager <id> - отключить менеджера"
    )


@router.message(Command("managers_full"))
async def cmd_managers_full(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    rows = await list_managers()
    if not rows:
        return await message.answer("Менеджеры не найдены.")
    text = ["<b>Список менеджеров</b>"]
    for row in rows:
        text.append(
            f"ID: {row['telegram_id']}\n"
            f"Имя: {row['name']}\n"
            f"Username: @{row['username'] or 'нет'}\n"
            f"Роль: {row['role']}\n"
            f"Активен: {'да' if row['is_active'] else 'нет'}\n"
        )
    await message.answer("\n".join(text), parse_mode="HTML")


@router.message(Command("stats_all"))
async def cmd_stats_all(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    rows = await get_all_stats()
    await message.answer(format_stats(rows), parse_mode="HTML")