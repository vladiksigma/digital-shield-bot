"""
Телеграм-бот «Цифровой щит»
Чат-бот для противодействия интернет-мошенничеству среди подростков.
"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# ============================================================
#  НАСТРОЙКИ
# ============================================================

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise RuntimeError("Переменная окружения BOT_TOKEN не задана!")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ============================================================
#  ТЕКСТЫ И ДАННЫЕ
# ============================================================

WELCOME_TEXT = (
    "Привет! Я — <b>Цифровой Щит</b> 🛡\n\n"
    "Помогу тебе защититься от мошенников в интернете.\n\n"
    "Выбери тему, которая тебя интересует:"
)

PHISHING_TEXT = (
    "<b>Что такое фишинг?</b>\n\n"
    "Фишинг — это вид мошенничества, когда злоумышленники создают "
    "поддельные сайты или отправляют ложные сообщения, чтобы украсть "
    "твои логин, пароль или данные банковской карты.\n\n"
    "<b>Как распознать фишинг:</b>\n"
    "• Проверяй адрес сайта — мошенники меняют одну-две буквы "
    "(например, vk0ntakte.ru вместо vk.com)\n"
    "• Не переходи по ссылкам из подозрительных сообщений\n"
    "• Не вводи пароль, если сайт выглядит «не так, как обычно»\n"
    "• Обрати внимание на ошибки в тексте и странный дизайн\n\n"
    "<b>Примеры фишинга:</b>\n"
    "• Сообщение «Ваш аккаунт заблокирован, перейдите по ссылке»\n"
    "• Письмо от «службы поддержки» с просьбой подтвердить пароль\n"
    "• Поддельный сайт онлайн-игры для «бесплатных скинов»\n\n"
    "<b>Что делать, если попался:</b>\n"
    "1. Немедленно смени пароль на настоящем сайте\n"
    "2. Включи двухфакторную аутентификацию\n"
    "3. Расскажи родителям или учителю"
)

PAYMENTS_TEXT = (
    "<b>Безопасные платежи</b>\n\n"
    "Правила безопасных покупок и платежей в интернете:\n\n"
    "<b>Основные правила:</b>\n"
    "• Никогда не сообщай CVV-код карты (3 цифры на обороте) "
    "незнакомым людям\n"
    "• Не отправляй фото банковской карты в мессенджерах\n"
    "• Используй виртуальные карты для онлайн-покупок\n"
    "• Покупай только на проверенных сайтах (ищи значок замка "
    "в адресной строке — https)\n\n"
    "<b>Красные флаги:</b>\n"
    "• Продавец просит перевести деньги на личную карту\n"
    "• Цена слишком хорошая, чтобы быть правдой\n"
    "• Просят внести «страховой взнос» или «комиссию» заранее\n"
    "• Торопят с оплатой: «осталось 5 минут!»\n\n"
    "<b>Совет:</b> Попроси родителей завести тебе отдельную карту "
    "для интернет-покупок с небольшим лимитом."
)

ACCOUNT_TEXT = (
    "<b>Защита аккаунта</b>\n\n"
    "Как надёжно защитить свои аккаунты в соцсетях и играх:\n\n"
    "<b>Пароль:</b>\n"
    "• Используй длинные пароли (12+ символов): буквы, цифры, спецсимволы\n"
    "• Не используй один пароль для всех сайтов\n"
    "• Не используй в пароле дату рождения, имя или «123456»\n"
    "• Меняй пароли хотя бы раз в полгода\n\n"
    "<b>Двухфакторная аутентификация (2FA):</b>\n"
    "• Включи её везде, где это возможно (ВК, Телеграм, почта, игры)\n"
    "• Используй приложение-аутентификатор, а не только СМС\n\n"
    "<b>Общие правила:</b>\n"
    "• Не давай свой пароль друзьям — даже лучшим\n"
    "• Не входи в свои аккаунты с чужих устройств\n"
    "• Проверяй активные сессии в настройках аккаунта\n"
    "• Не устанавливай подозрительные приложения и расширения"
)

HELP_TEXT = (
    "<b>Куда обратиться за помощью?</b>\n\n"
    "Если ты столкнулся с мошенничеством или чувствуешь опасность:\n\n"
    "<b>Телефоны доверия:</b>\n"
    "• <b>8-800-2000-122</b> — бесплатная линия помощи детям и подросткам "
    "(круглосуточно)\n"
    "• <b>112</b> — единый номер экстренных служб\n\n"
    "<b>Онлайн-ресурсы:</b>\n"
    "• <a href='https://pd.rkn.gov.ru/'>Роскомнадзор — защита персональных "
    "данных</a>\n"
    "• <a href='https://kiberbez.ru/'>Кибербезопасность.рф</a> — портал "
    "цифровой грамотности\n\n"
    "<b>Что делать прямо сейчас:</b>\n"
    "1. Расскажи родителям или другому взрослому, которому доверяешь\n"
    "2. Сделай скриншоты переписки с мошенником\n"
    "3. Заблокируй мошенника и пожалуйся на него в соцсети\n"
    "4. Если украли деньги — обратись в банк и полицию\n\n"
    "<b>Помни:</b> ты не виноват! Мошенники — профессионалы обмана. "
    "Обратиться за помощью — это правильно и смело."
)

SCHEMES_TEXT = (
    "<b>Популярные схемы мошенников</b>\n\n"
    "Вот самые распространённые способы обмана подростков:\n\n"
    "<b>1. Фишинг в играх</b>\n"
    "Поддельный сайт для входа в аккаунт игры → кража логина, пароля "
    "и привязанной карты родителей.\n\n"
    "<b>2. Ложные конкурсы и розыгрыши</b>\n"
    "«Выиграй iPhone! Просто введи код из СМС» → передача доступа "
    "к аккаунту или деньгам.\n\n"
    "<b>3. Шантаж в соцсетях</b>\n"
    "Знакомство → получение личных фото → требование денег под угрозой "
    "распространения.\n\n"
    "<b>4. Фейковый заработок</b>\n"
    "«Заработай 5000 руб. за час!» → просят «страховой взнос» или "
    "паспортные данные.\n\n"
    "<b>5. Подставные магазины</b>\n"
    "Очень дешёвые товары → оплата → товар никогда не приходит.\n\n"
    "Если что-то из этого произошло с тобой — не стесняйся, "
    "нажми <b>«Куда обратиться за помощью»</b>."
)

QUIZ_QUESTIONS = [
    {
        "question": "Тебе пишет «служба поддержки ВК» и просит назвать пароль. Что делать?",
        "options": [
            ("Назвать пароль — это же поддержка!", "quiz_1_wrong"),
            ("Не отвечать и заблокировать — настоящая поддержка никогда не просит пароль", "quiz_1_right"),
        ],
    },
    {
        "question": "Ты нашёл сайт, где продают кроссовки Nike за 500 руб. Стоит покупать?",
        "options": [
            ("Нет — слишком низкая цена, скорее всего мошенники", "quiz_2_right"),
            ("Да — какая удача, надо брать скорее!", "quiz_2_wrong"),
        ],
    },
    {
        "question": "Друг просит через сообщение одолжить денег на карту. Что сделать в первую очередь?",
        "options": [
            ("Сразу перевести — друг же просит!", "quiz_3_wrong"),
            ("Позвонить другу по телефону и убедиться, что это действительно он", "quiz_3_right"),
        ],
    },
]

# ============================================================
#  КЛАВИАТУРЫ
# ============================================================

def get_main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Что такое фишинг?", callback_data="phishing")],
        [InlineKeyboardButton(text="Безопасные платежи", callback_data="payments")],
        [InlineKeyboardButton(text="Защита аккаунта", callback_data="account")],
        [InlineKeyboardButton(text="Куда обратиться за помощью?", callback_data="help")],
        [InlineKeyboardButton(text="Схемы мошенников", callback_data="schemes")],
        [InlineKeyboardButton(text="Проверь себя (викторина)", callback_data="quiz_start")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="« Назад в меню", callback_data="menu")]
        ]
    )


def get_quiz_keyboard(question_index: int) -> InlineKeyboardMarkup:
    q = QUIZ_QUESTIONS[question_index]
    buttons = [
        [InlineKeyboardButton(text=text, callback_data=data)]
        for text, data in q["options"]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_quiz_next_keyboard(next_index: int) -> InlineKeyboardMarkup:
    if next_index < len(QUIZ_QUESTIONS):
        buttons = [
            [InlineKeyboardButton(text="Следующий вопрос »", callback_data=f"quiz_{next_index}")],
            [InlineKeyboardButton(text="« Назад в меню", callback_data="menu")],
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="Пройти ещё раз", callback_data="quiz_start")],
            [InlineKeyboardButton(text="« Назад в меню", callback_data="menu")],
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ============================================================
#  ОБРАБОТЧИКИ
# ============================================================

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        HELP_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )


@router.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        WELCOME_TEXT,
        reply_markup=get_main_menu(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "phishing")
async def cb_phishing(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        PHISHING_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "payments")
async def cb_payments(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        PAYMENTS_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "account")
async def cb_account(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        ACCOUNT_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        HELP_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.callback_query(F.data == "schemes")
async def cb_schemes(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        SCHEMES_TEXT,
        reply_markup=get_back_button(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "quiz_start")
async def cb_quiz_start(callback: CallbackQuery) -> None:
    q = QUIZ_QUESTIONS[0]
    await callback.message.edit_text(
        f"<b>Викторина «Проверь себя»</b>\n\n"
        f"Вопрос 1 из {len(QUIZ_QUESTIONS)}:\n\n"
        f"{q['question']}",
        reply_markup=get_quiz_keyboard(0),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("quiz_") & ~F.data.in_({"quiz_start"}))
async def cb_quiz_navigate(callback: CallbackQuery) -> None:
    parts = callback.data.split("_")
    if len(parts) == 2 and parts[1].isdigit():
        idx = int(parts[1])
        if idx < len(QUIZ_QUESTIONS):
            q = QUIZ_QUESTIONS[idx]
            await callback.message.edit_text(
                f"<b>Викторина «Проверь себя»</b>\n\n"
                f"Вопрос {idx + 1} из {len(QUIZ_QUESTIONS)}:\n\n"
                f"{q['question']}",
                reply_markup=get_quiz_keyboard(idx),
                parse_mode="HTML",
            )
    elif len(parts) == 3:
        q_idx = int(parts[1]) - 1
        is_right = parts[2] == "right"
        next_idx = q_idx + 1

        if is_right:
            text = "Правильно! Молодец, ты разбираешься в цифровой безопасности."
        else:
            text = (
                "Неправильно! Будь внимательнее — мошенники рассчитывают "
                "именно на поспешные решения."
            )

        if next_idx >= len(QUIZ_QUESTIONS):
            text += "\n\nВикторина завершена! Теперь ты лучше знаешь, как защитить себя в интернете."

        await callback.message.edit_text(
            text,
            reply_markup=get_quiz_next_keyboard(next_idx),
            parse_mode="HTML",
        )

    await callback.answer()


@router.message()
async def on_any_message(message: Message) -> None:
    await message.answer(
        "Я пока умею отвечать только по кнопкам меню.\n"
        "Нажми /start или /menu, чтобы открыть главное меню.",
        parse_mode="HTML",
    )


# ============================================================
#  ЗАПУСК
# ============================================================

async def main() -> None:
    logger.info("Бот «Цифровой щит» запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
