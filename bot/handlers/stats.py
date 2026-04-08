from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.manager_service import manager_has_access
from bot.services.stats_service import get_all_stats, get_manager_stats
from bot.utils.formatters import format_stats

router = Router()


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not await manager_has_access(message.from_user.id):
        return await message.answer("Нет доступа.")
    rows = await get_all_stats()
    await message.answer(format_stats(rows), parse_mode="HTML")


@router.message(Command("stats_me"))
async def cmd_stats_me(message: Message):
    if not await manager_has_access(message.from_user.id):
        return await message.answer("Нет доступа.")
    row = await get_manager_stats(message.from_user.id)
    if not row:
        return await message.answer("Статистика не найдена.")
    await message.answer(format_stats([row]), parse_mode="HTML")