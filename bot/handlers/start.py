from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.main_menu import main_menu_kb, manager_menu_kb, reply_menu_kb, manager_reply_kb
from bot.config import MANAGER_CHAT_ID

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    args = message.text.split()

    # Пришёл с сайта через кнопку "Задать вопрос" — первым!
    if len(args) > 1 and args[1] == "question":
        from bot.handlers.orders import QuestionForm
        await message.answer(
            "👋 Здравствуйте!\n\n"
            "Вы можете задать любой вопрос менеджеру — он ответит вам в ближайшее время.\n\n"
            "✍️ Напишите ваш вопрос:",
            parse_mode="HTML"
        )
        await state.set_state(QuestionForm.waiting)
        return

    # Менеджер
    if message.from_user.id == MANAGER_CHAT_ID:
        await message.answer(
            "👨‍💼 <b>Панель менеджера STEM Academia</b>\n\nВыберите действие:",
            parse_mode="HTML",
            reply_markup=manager_reply_kb()
        )
        await message.answer(
            "📋 Или выберите из меню:",
            reply_markup=manager_menu_kb()
        )
    # Обычный клиент
    else:
        await message.answer(
            "👋 Добро пожаловать в <b>STEM Academia</b>!\n\n"
            "Мы поставляем мебель, технику и декор для школ и образовательных учреждений.\n\n"
            "📍 г.Астана, ул.Домалак-ана 26\n"
            "📞 +7 (700) 088 0132\n\n"
            "Выберите раздел каталога:",
            parse_mode="HTML",
            reply_markup=reply_menu_kb()
        )
        await message.answer(
            "📋 Или выберите из меню:",
            reply_markup=main_menu_kb()
        )
