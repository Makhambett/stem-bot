from aiogram import Bot
from bot.config import settings
from bot.keyboards.request_kb import new_request_kb
from bot.utils.formatters import format_request_card


async def notify_new_request(bot: Bot, request: dict):
    text = format_request_card(request)
    await bot.send_message(
        chat_id=settings.managers_group_id,
        text=text,
        parse_mode="HTML",
        reply_markup=new_request_kb(request["id"]),
    )