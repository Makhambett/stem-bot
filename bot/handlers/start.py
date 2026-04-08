from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.services.manager_service import manager_has_access, is_admin

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if await is_admin(message.from_user.id):
        return await message.answer(
            "Привет, админ. Доступны команды:\n"
            "/managers - список менеджеров\n"
            "/remove_manager <id> - отключить менеджера\n"
            "/stats - общая статистика\n"
            "/stats_me - моя статистика"
        )

    if await manager_has_access(message.from_user.id):
        return await message.answer(
            "Привет, менеджер. Доступны команды:\n"
            "/stats_me - моя статистика\n"
            "/stats - общая статистика"
        )

    await message.answer(
        "Здравствуйте.\n"
        "Если вы менеджер и уже добавлены в рабочую группу, отправьте /registr для регистрации."
    )