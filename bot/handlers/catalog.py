from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from bot.keyboards.main_menu import main_menu_kb
from bot.keyboards.catalog_kb import mebel_kb, decor_kb, electro_kb, order_kb
from bot.cart import add_to_cart, cart_count

router = Router()

ITEMS = {
    "item_divany":      ("🛋 Диваны",               "Мягкие диваны для офисов и школ.\nМатериал: ЛДСП, мягкая поверхность\nРазмеры: 2500x850x450\nАртикул: S.Me-ST.S.DP"),
    "item_kreslo":      ("🪑 Кресла",               "Эргономичные кресла.\nМатериал: ЛДСП панели, металлические ножки\nРазмеры: 850x700x700\nАртикул: S.Me-ST.S.DP"),
    "item_pufy":        ("📦 Пуфы",                 "Мягкие пуфы разных форм.\nМатериал: Поролон, ткань\nРазмеры: 400x400x400\nАртикул: S.Me-ST.S.DP"),
    "item_stellazhi":   ("📚 Стеллажи",             "Открытые стеллажи для классов.\nМатериал: ЛДСП\nРазмеры: 2000x800x300\nАртикул: S.Me-ST.S.DP"),
    "item_tumby":       ("🗄 Тумбы",                "Тумбы с ящиками.\nМатериал: ЛДСП\nРазмеры: 750x400x450\nАртикул: S.Me-ST.S.DP"),
    "item_stulya":      ("🪑 Стулья",               "Школьные и офисные стулья.\nМатериал: Металл, пластик\nРазмеры: 820x380x380\nАртикул: S.Me-ST.S.DP"),
    "item_shkafy":      ("🚪 Шкафы",               "Встроенные и стандартные шкафы.\nМатериал: ЛДСП, МДФ\nРазмеры: 2000x800x500\nАртикул: S.Me-ST.S.DP"),
    "item_kuhnya":      ("🍳 Кухня",               "Кухонные гарнитуры.\nМатериал: ЛДСП, МДФ\nРазмеры: по проекту\nАртикул: S.Me-ST.S.DP"),
    "item_stoly":       ("🪵 Столы",               "Обеденные и рабочие столы.\nМатериал: ЛДСП, металл\nРазмеры: 1200x600x750\nАртикул: S.Me-ST.S.DP"),
    "item_gos":         ("🏛 ГОС символика",        "Государственная символика РК.\nМатериал: ЛДСП, МДФ\nРазмеры: 2000x2500\nАртикул: S.Me-ST.S.DP"),
    "item_3dpanels":    ("🧱 3D панели",            "Декоративные 3D панели.\nМатериал: Гипс\nРазмеры: 600x600\nАртикул: S.Me-ST.S.DP"),
    "item_lighting":    ("💡 Освещение",            "LED светильники и ленты.\nРазмеры: различные\nАртикул: S.Me-ST.S.DP"),
    "item_peregorodki": ("🪟 Перегородки",          "Офисные перегородки.\nМатериал: Стекло, алюминий\nАртикул: S.Me-ST.S.DP"),
    "item_rasteniya":   ("🪴 Растения",             "Искусственные и живые растения.\nАртикул: S.Me-ST.S.DP"),
    "item_shtory":      ("🎭 Шторы",               "Рулонные и тканевые шторы.\nАртикул: S.Me-ST.S.DP"),
    "item_doski":       ("📋 Доски",               "Маркерные и меловые доски.\nАртикул: S.Me-ST.S.DP"),
    "item_interactive": ("📺 Интерактивные панели", "Интерактивные панели для классов.\nАртикул: S.Me-ST.S.DP"),
    "item_computers":   ("💻 Компьютеры",           "Компьютеры и ноутбуки.\nАртикул: S.Me-ST.S.DP"),
    "item_infokiosk":   ("🖥 Инфо киоск",           "Информационные киоски.\nАртикул: S.Me-ST.S.DP"),
    "item_stanki":      ("⚙️ Станки",              "Учебные станки.\nАртикул: S.Me-ST.S.DP"),
    "item_bytovaya":    ("🏠 Бытовая техника",      "Бытовая техника для школ.\nАртикул: S.Me-ST.S.DP"),
    "item_printers3d":  ("🖨 3Д принтеры",          "3D принтеры для обучения.\nАртикул: S.Me-ST.S.DP"),
}

BASE  = r"C:\Users\tnyss\OneDrive\Рабочий стол\diplomcode\stem-catalog\public\img\pagesecond"
DECOR = r"C:\Users\tnyss\OneDrive\Рабочий стол\diplomcode\stem-catalog\public\img\pagedecor"

DESC      = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
MATERIALS = "• Синтепон\n• Мягкая поверхность\n• Велкор\n• Пластмассовые ножки"
COLORS    = "🟠 Оранжевый  🟡 Бежевый  🟢 Тёмно-зелёный  ⚫ Серый"

CARDS = {
    # ─── МЕБЕЛЬ ───────────────────────────────────────────
    "item_divany": [
        {"name": "🛋 ДИВАН 1", "desc": DESC, "materials": MATERIALS, "sizes": "2500x850x450", "colors": COLORS, "article": "L.Me-DI.UN.2500", "photo": FSInputFile(rf"{BASE}\divany\divan1.png")},
        {"name": "🛋 ДИВАН 2", "desc": DESC, "materials": MATERIALS, "sizes": "2500x850x450", "colors": COLORS, "article": "L.Me-DI.UN.2500", "photo": FSInputFile(rf"{BASE}\divany\divan2.png")},
        {"name": "🛋 ДИВАН 3", "desc": DESC, "materials": MATERIALS, "sizes": "2500x850x450", "colors": COLORS, "article": "L.Me-DI.UN.2500", "photo": FSInputFile(rf"{BASE}\divany\divan3.png")},
        {"name": "🛋 ДИВАН 4", "desc": DESC, "materials": MATERIALS, "sizes": "2500x850x450", "colors": COLORS, "article": "L.Me-DI.UN.2500", "photo": FSInputFile(rf"{BASE}\divany\divan4.png")},
        {"name": "🛋 ДИВАН 5", "desc": DESC, "materials": MATERIALS, "sizes": "2500x850x450", "colors": COLORS, "article": "L.Me-DI.UN.2500", "photo": FSInputFile(rf"{BASE}\divany\divan5.png")},
    ],
    "item_kreslo": [
        {"name": "🪑 КРЕСЛО 1", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo1.png")},
        {"name": "🪑 КРЕСЛО 2", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo2.png")},
        {"name": "🪑 КРЕСЛО 3", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo3.png")},
        {"name": "🪑 КРЕСЛО 4", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo4.png")},
        {"name": "🪑 КРЕСЛО 5", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo5.png")},
        {"name": "🪑 КРЕСЛО 6", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo6.png")},
        {"name": "🪑 КРЕСЛО 7", "desc": DESC, "materials": MATERIALS, "sizes": "850x700x700", "colors": COLORS, "article": "L.Me-KR.UN.850", "photo": FSInputFile(rf"{BASE}\kreslo\kreslo7.png")},
    ],
    "item_pufy": [
        {"name": "📦 ПУФ 1", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf1.png")},
        {"name": "📦 ПУФ 2", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf2.png")},
        {"name": "📦 ПУФ 3", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf3.png")},
        {"name": "📦 ПУФ 4", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf4.png")},
        {"name": "📦 ПУФ 5", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf5.png")},
        {"name": "📦 ПУФ 6", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf6.png")},
        {"name": "📦 ПУФ 7", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf7.png")},
        {"name": "📦 ПУФ 8", "desc": DESC, "materials": MATERIALS, "sizes": "400x400x400", "colors": COLORS, "article": "L.Me-PU.UN.400", "photo": FSInputFile(rf"{BASE}\pufy\puf8.png")},
    ],
    "item_stellazhi": [
        {"name": "📚 СТЕЛЛАЖ 1", "desc": DESC, "materials": MATERIALS, "sizes": "2000x800x300", "colors": COLORS, "article": "L.Me-ST.UN.2000", "photo": FSInputFile(rf"{BASE}\stellazhi\stellazhi1.png")},
        {"name": "📚 СТЕЛЛАЖ 2", "desc": DESC, "materials": MATERIALS, "sizes": "2000x800x300", "colors": COLORS, "article": "L.Me-ST.UN.2000", "photo": FSInputFile(rf"{BASE}\stellazhi\stellazhi2.png")},
        {"name": "📚 СТЕЛЛАЖ 3", "desc": DESC, "materials": MATERIALS, "sizes": "2000x800x300", "colors": COLORS, "article": "L.Me-ST.UN.2000", "photo": FSInputFile(rf"{BASE}\stellazhi\stellazhi.3.png")},
    ],
    "item_tumby": [
        {"name": "🗄 ТУМБА 1", "desc": DESC, "materials": MATERIALS, "sizes": "750x400x450", "colors": COLORS, "article": "L.Me-TU.UN.750", "photo": FSInputFile(rf"{BASE}\tumby\tumba1.png")},
        {"name": "🗄 ТУМБА 2", "desc": DESC, "materials": MATERIALS, "sizes": "750x400x450", "colors": COLORS, "article": "L.Me-TU.UN.750", "photo": FSInputFile(rf"{BASE}\tumby\tumba2.png")},
    ],

    # ─── ДЕКОР ────────────────────────────────────────────
    "item_gos": [
        {"name": "🏛 ГОС символика 1", "desc": DESC, "materials": "• ЛДСП\n• МДФ", "sizes": "2000x2500", "colors": COLORS, "article": "L.Me-GOS.UN.1", "photo": FSInputFile(rf"{DECOR}\gos\gos1.png")},
        {"name": "🏛 ГОС символика 2", "desc": DESC, "materials": "• ЛДСП\n• МДФ", "sizes": "2000x2500", "colors": COLORS, "article": "L.Me-GOS.UN.2", "photo": FSInputFile(rf"{DECOR}\gos\gos2.png")},
        {"name": "🏛 ГОС символика 3", "desc": DESC, "materials": "• ЛДСП\n• МДФ", "sizes": "2000x2500", "colors": COLORS, "article": "L.Me-GOS.UN.3", "photo": FSInputFile(rf"{DECOR}\gos\gos3.png")},
    ],
    "item_3dpanels": [
        {"name": "🧱 3D панель Фигурный",  "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.figurny",   "photo": FSInputFile(rf"{DECOR}\3dpanels\figurny.png")},
        {"name": "🧱 3D панель Линейный",  "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.lineyny",   "photo": FSInputFile(rf"{DECOR}\3dpanels\lineyny.png")},
        {"name": "🧱 3D панель Реечный",   "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.reechny",   "photo": FSInputFile(rf"{DECOR}\3dpanels\reechny.png")},
        {"name": "🧱 3D панель Рельефный", "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.relefny",   "photo": FSInputFile(rf"{DECOR}\3dpanels\relefny.png")},
        {"name": "🧱 3D панель Узорчатый", "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.uzorchaty", "photo": FSInputFile(rf"{DECOR}\3dpanels\uzoorchaty.png")},
        {"name": "🧱 3D панель Волнистый", "desc": DESC, "materials": "• Гипс", "sizes": "600x600", "colors": COLORS, "article": "L.Me-3D.volnisty",  "photo": FSInputFile(rf"{DECOR}\3dpanels\volnisty.png")},
    ],
    "item_lighting": [
        {"name": "💡 Arkoslight",      "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.arkoslight",     "photo": FSInputFile(rf"{DECOR}\lighting\arkoslight.png")},
        {"name": "💡 Aura",            "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.aura",            "photo": FSInputFile(rf"{DECOR}\lighting\aura.png")},
        {"name": "💡 DK-LED",          "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.dk-led",          "photo": FSInputFile(rf"{DECOR}\lighting\dk-led.png")},
        {"name": "💡 Elektrostandard", "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.elektrostandard", "photo": FSInputFile(rf"{DECOR}\lighting\elektrostandard.png")},
        {"name": "💡 ERA",             "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.era",             "photo": FSInputFile(rf"{DECOR}\lighting\era.png")},
        {"name": "💡 LED ленты",       "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.led-lenty",       "photo": FSInputFile(rf"{DECOR}\lighting\led-lenty.png")},
        {"name": "💡 LED Oval",        "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.led-oval",        "photo": FSInputFile(rf"{DECOR}\lighting\led-oval.png")},
        {"name": "💡 LEDS-C4",         "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.leds-c4",         "photo": FSInputFile(rf"{DECOR}\lighting\leds-c4.png")},
        {"name": "💡 Lezard",          "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.lezard",          "photo": FSInputFile(rf"{DECOR}\lighting\lezard.png")},
        {"name": "💡 Lezard 2",        "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.lezard2",         "photo": FSInputFile(rf"{DECOR}\lighting\lezard2.png")},
        {"name": "💡 Rullo",           "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.rullo",           "photo": FSInputFile(rf"{DECOR}\lighting\rullo.png")},
        {"name": "💡 Start",           "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.start",           "photo": FSInputFile(rf"{DECOR}\lighting\start.png")},
        {"name": "💡 Start 2",         "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.start2",          "photo": FSInputFile(rf"{DECOR}\lighting\start2.png")},
        {"name": "💡 Start 3",         "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.start3",          "photo": FSInputFile(rf"{DECOR}\lighting\start3.png")},
        {"name": "💡 Tekled",          "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.tekled",          "photo": FSInputFile(rf"{DECOR}\lighting\tekled.png")},
        {"name": "💡 Volta",           "desc": DESC, "materials": "• LED", "sizes": "различные", "colors": COLORS, "article": "L.Me-LI.volta",           "photo": FSInputFile(rf"{DECOR}\lighting\volta.png")},
    ],
    "item_peregorodki": [
        {"name": "🪟 Перегородка 1", "desc": DESC, "materials": "• Стекло\n• Алюминий", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-PE.item2",  "photo": FSInputFile(rf"{DECOR}\peregorodki\item2.png")},
        {"name": "🪟 Перегородка 2", "desc": DESC, "materials": "• Стекло\n• Алюминий", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-PE.item31", "photo": FSInputFile(rf"{DECOR}\peregorodki\item31.png")},
        {"name": "🪟 Перегородка 3", "desc": DESC, "materials": "• Стекло\n• Алюминий", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-PE.item32", "photo": FSInputFile(rf"{DECOR}\peregorodki\item32.png")},
    ],
    "item_rasteniya": [
        {"name": "🪴 Растение 1", "desc": DESC, "materials": "• Натуральные материалы", "sizes": "различные", "colors": COLORS, "article": "L.Me-RA.item1", "photo": FSInputFile(rf"{DECOR}\rasteniya\item1.png")},
        {"name": "🪴 Растение 2", "desc": DESC, "materials": "• Натуральные материалы", "sizes": "различные", "colors": COLORS, "article": "L.Me-RA.item2", "photo": FSInputFile(rf"{DECOR}\rasteniya\item2.png")},
        {"name": "🪴 Растение 3", "desc": DESC, "materials": "• Натуральные материалы", "sizes": "различные", "colors": COLORS, "article": "L.Me-RA.item3", "photo": FSInputFile(rf"{DECOR}\rasteniya\item3.png")},
    ],
    "item_shtory": [
        {"name": "🎭 Штора 1", "desc": DESC, "materials": "• Ткань\n• Рулонный механизм", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-SH.item1", "photo": FSInputFile(rf"{DECOR}\shtory\item1.png")},
        {"name": "🎭 Штора 2", "desc": DESC, "materials": "• Ткань\n• Рулонный механизм", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-SH.item2", "photo": FSInputFile(rf"{DECOR}\shtory\item2.png")},
        {"name": "🎭 Штора 3", "desc": DESC, "materials": "• Ткань\n• Рулонный механизм", "sizes": "по проекту", "colors": COLORS, "article": "L.Me-SH.item3", "photo": FSInputFile(rf"{DECOR}\shtory\item3.png")},
    ],
    "item_doski": [
        {"name": "📋 Доска 1", "desc": DESC, "materials": "• Металл\n• Пластик", "sizes": "различные", "colors": COLORS, "article": "L.Me-DO.item1", "photo": FSInputFile(rf"{DECOR}\doski\item1.png")},
        {"name": "📋 Доска 2", "desc": DESC, "materials": "• Металл\n• Пластик", "sizes": "различные", "colors": COLORS, "article": "L.Me-DO.item2", "photo": FSInputFile(rf"{DECOR}\doski\item2.png")},
        {"name": "📋 Доска 3", "desc": DESC, "materials": "• Металл\n• Пластик", "sizes": "различные", "colors": COLORS, "article": "L.Me-DO.item3", "photo": FSInputFile(rf"{DECOR}\doski\item3.png")},
    ],
}


@router.callback_query(F.data == "main_menu")
async def main_menu(call: CallbackQuery):
    await call.answer()
    count = cart_count(call.from_user.id)
    try:
        await call.message.edit_text("Выберите раздел каталога:", reply_markup=main_menu_kb(count))
    except TelegramBadRequest:
        await call.message.delete()
        await call.message.answer("Выберите раздел каталога:", reply_markup=main_menu_kb(count))


@router.callback_query(F.data == "cat_mebel")
async def cat_mebel(call: CallbackQuery):
    await call.message.edit_text("🪑 <b>Мебель</b>\nВыберите категорию:", parse_mode="HTML", reply_markup=mebel_kb())


@router.callback_query(F.data == "cat_decor")
async def cat_decor(call: CallbackQuery):
    await call.message.edit_text("🎨 <b>Декор</b>\nВыберите категорию:", parse_mode="HTML", reply_markup=decor_kb())


@router.callback_query(F.data == "cat_electro")
async def cat_electro(call: CallbackQuery):
    await call.message.edit_text("💡 <b>Электротехника</b>\nВыберите категорию:", parse_mode="HTML", reply_markup=electro_kb())


@router.callback_query(F.data.startswith("item_"))
async def show_item(call: CallbackQuery):
    key = call.data
    await call.answer()

    if key in CARDS:
        try:
            await call.message.delete()
        except TelegramBadRequest:
            pass

        for i, p in enumerate(CARDS[key]):
            caption = (
                f"<b>{p['name']}</b>\n\n"
                f"{p['desc']}\n\n"
                f"📦 <b>Материал:</b>\n{p['materials']}\n\n"
                f"📐 <b>Размеры:</b> {p['sizes']}\n"
                f"🎨 <b>Цвет:</b> {p['colors']}\n"
                f"🔖 <b>Артикул:</b> {p['article']}"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🛒 В корзину", callback_data=f"cart_add_{key}_{i}")],
                [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="main_menu")]
            ])
            await call.message.answer_photo(
                photo=p["photo"],
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )
    else:
        name, desc = ITEMS[key]
        await call.message.edit_text(
            f"<b>{name}</b>\n\n{desc}",
            parse_mode="HTML",
            reply_markup=order_kb(key)
        )


@router.callback_query(F.data.startswith("cart_add_"))
async def cart_add(call: CallbackQuery):
    parts = call.data.split("_")
    # cart_add_item_divany_0 → ['cart', 'add', 'item', 'divany', '0']
    idx = int(parts[-1])
    key = "_".join(parts[2:-1])  # item_divany

    if key not in CARDS or idx >= len(CARDS[key]):
        await call.answer("Ошибка!")
        return

    product = CARDS[key][idx]
    add_to_cart(call.from_user.id, {
        "name": product["name"],
        "article": product["article"],
        "sizes": product["sizes"],
    })

    count = cart_count(call.from_user.id)
    await call.answer(f"✅ Добавлено! В корзине: {count} товар(а)", show_alert=False)
