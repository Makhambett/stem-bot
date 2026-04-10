import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.repositories.metrics import get_daily_stats, get_fail_reasons, get_top_managers
from bot.utils.formatters import format_daily_stats, format_fail_reasons, format_top_managers

router = Router()

# 🟢 Читаем ADMIN_ID напрямую из .env (безопасно и не ломает импорт)
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

def is_admin_private(message: Message) -> bool:
    """Проверка: личный чат + совпадение ID админа"""
    return message.chat.type == "private" and message.from_user.id == ADMIN_ID


@router.message(Command("daily_stats"))
async def cmd_daily_stats(message: Message):
    if not is_admin_private(message):
        return  # Молча игнорируем, если не админ или не личка
    stats = await get_daily_stats()
    await message.answer(format_daily_stats(stats), parse_mode="HTML")


@router.message(Command("fail_stats"))
async def cmd_fail_stats(message: Message):
    if not is_admin_private(message):
        return
    reasons = await get_fail_reasons()
    await message.answer(format_fail_reasons(reasons), parse_mode="HTML")


@router.message(Command("top_managers"))
async def cmd_top_managers(message: Message):
    if not is_admin_private(message):
        return
    managers = await get_top_managers()
    await message.answer(format_top_managers(managers), parse_mode="HTML")