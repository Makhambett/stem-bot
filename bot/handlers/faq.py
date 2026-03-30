from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.main_menu import back_kb

router = Router()

@router.callback_query(F.data == "faq")
async def faq(call: CallbackQuery):
    await call.message.edit_text(
        "📞 <b>Контакты STEM Academia</b>\n\n"
        "📍 Адрес: г.Астана, ул.Домалак-ана 26\n"
        "📞 Телефон: +7 (700) 088 0132\n"
        "🕐 Режим работы: Пн-Пт 9:00-18:00\n\n"
        "🌐 Сайт: stem-academia.kz\n"
        "📸 Instagram: @stem_academia\n"
        "▶️ YouTube: STEM Academia",
        parse_mode="HTML",
        reply_markup=back_kb()
    )
