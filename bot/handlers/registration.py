from aiogram import Router
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.repositories.managers import get_manager, upsert_manager
from bot.services.manager_service import (
    deactivate_manager,
    is_admin,
    is_user_in_managers_group,
    list_managers,
    register_manager_by_id,
)
from bot.states.registration import RegistrationState

router = Router()


@router.message(Command("registr"))
async def cmd_registr(message: Message, state: FSMContext):
    if message.chat.type != ChatType.PRIVATE:
        return await message.answer("Регистрация менеджера доступна только в личке с ботом.")

    existing_manager = await get_manager(message.from_user.id)
    if existing_manager and existing_manager["is_active"]:
        return await message.answer("Вы уже зарегистрированы как менеджер.")

    is_member = await is_user_in_managers_group(message.bot, message.from_user.id)
    if not is_member:
        return await message.answer(
            "Вы не состоите в рабочей группе менеджеров.\n"
            "Сначала администратор должен добавить вас в группу."
        )

    await state.set_state(RegistrationState.waiting_for_name)
    await message.answer("Введите ваше имя для регистрации менеджера:")


@router.message(RegistrationState.waiting_for_name)
async def process_manager_name(message: Message, state: FSMContext):
    if message.chat.type != ChatType.PRIVATE:
        return await message.answer("Продолжите регистрацию в личных сообщениях с ботом.")

    name = (message.text or "").strip()

    if len(name) < 2:
        return await message.answer("Имя слишком короткое. Введите корректное имя.")

    await upsert_manager(
        telegram_id=message.from_user.id,
        name=name,
        username=message.from_user.username,
        role="manager",
    )

    await state.clear()
    await message.answer(
        f"Вы зарегистрированы как менеджер.\n"
        f"Имя: {name}\n"
        f"Telegram ID: {message.from_user.id}"
    )


@router.message(Command("register_manager"))
async def cmd_register_manager(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Используй: /register_manager <telegram_id>")
    telegram_id = int(parts[1])
    row = await register_manager_by_id(message.bot, telegram_id, role="manager")
    await message.answer(f"Менеджер зарегистрирован: {row['name']} ({row['telegram_id']})")


@router.message(Command("remove_manager"))
async def cmd_remove_manager(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Используй: /remove_manager <telegram_id>")
    telegram_id = int(parts[1])
    await deactivate_manager(telegram_id)
    await message.answer(f"Менеджер {telegram_id} деактивирован.")


@router.message(Command("managers"))
async def cmd_managers(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.answer("Нет доступа.")
    rows = await list_managers()
    if not rows:
        return await message.answer("Менеджеры не найдены.")
    text = "\n".join(
        f"{row['name']} | {row['telegram_id']} | {row['role']} | active={row['is_active']}"
        for row in rows
    )
    await message.answer(text)