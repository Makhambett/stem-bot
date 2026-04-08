from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from bot.config import settings
from bot.repositories.managers import get_manager, list_managers, upsert_manager, deactivate_manager


async def sync_default_staff(bot: Bot):
    admin_chat = await bot.get_chat(settings.admin_id)
    await upsert_manager(
        telegram_id=settings.admin_id,
        name=admin_chat.full_name,
        username=admin_chat.username,
        role="admin",
    )


async def register_manager_by_id(bot: Bot, telegram_id: int, role: str = "manager"):
    chat = await bot.get_chat(telegram_id)
    return await upsert_manager(
        telegram_id=telegram_id,
        name=chat.full_name,
        username=chat.username,
        role=role,
    )


async def manager_has_access(telegram_id: int) -> bool:
    manager = await get_manager(telegram_id)
    return bool(manager and manager["is_active"])


async def is_admin(telegram_id: int) -> bool:
    manager = await get_manager(telegram_id)
    return bool(manager and manager["role"] == "admin" and manager["is_active"])


async def is_user_in_managers_group(bot: Bot, telegram_id: int) -> bool:
    try:
        member = await bot.get_chat_member(settings.managers_group_id, telegram_id)
        return member.status in {
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.RESTRICTED,
        }
    except Exception:
        return False


__all__ = [
    "sync_default_staff",
    "register_manager_by_id",
    "manager_has_access",
    "is_admin",
    "is_user_in_managers_group",
    "list_managers",
    "deactivate_manager",
    "get_manager",
]