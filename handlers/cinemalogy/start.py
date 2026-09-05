# handlers/cinemalogy/start.py

"""
Старт процесса Cinemalogy.
"""

from aiogram import Router
from aiogram.types import Message

from keyboards.cinemalogy.start import start_keyboard_v2

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter

router = Router()


async def start_cinemalogy(
    message: Message,
    source: str | None = None,
    telegram_id: int | None = None
):
    """
    Первый экран Cinemalogy.

    telegram_id — на случай, если message не от пользователя (например,
    это message бота при вызове из callback, как в cinemalogy_home):
    тогда message.from_user был бы ID бота, а не того, кто нажал кнопку.
    """

    if telegram_id is None:
        telegram_id = message.from_user.id

    # Записываем текущий шаг
    set_parameter(
        telegram_id,
        "current_step",
        "cinemalogy_start"
    )

    # Аналитика
    add_event(
        telegram_id,
        "cinemalogy_start",
        source
    )

    # # Текст — БЕЗ жирного, БЕЗ курсива, БЕЗ HTML
    # start_text = (
    #     "Добро пожаловать в мир синемалогии!\n\n"
    #     "Я – Гончарова Елизавета, EMDR‑терапевт, интегративный психолог "
    #     "проведу вас в тайны вашего бессознательного через культовые фильмы\n\n"
    #     "Я подготовила для вас интерактив, чтобы размяться перед кинопоказом\n\n"
    #     "Нажмите на кнопку «Выбрать кадр», чтобы начать"
    # )

    start_text = (
        "Добро пожаловать в Синемалогию!\n\n"
        "С вами я, Гончарова Елизавета, EMDR-терапевт, психолог, создатель Синемалогии ♥️\n\n"
        "В августе кинопраздник прошел очень изысканно. Увидеть атмосферу встречи можно в "
        "<a href=\"https://shaverinaa.ru/disk/sinemalogiya-0z6ljx\">фотографиях</a>\n\n"
        "Анонс предстоящей Синемалогии будет в моем "
        "<a href=\"https://t.me/your_mental_doc\">телеграм-канале</a> и "
        "<a href=\"https://www.instagram.com/your.mental.doc?igsi=YmhrNTdsNHg2bzVi&utm_source=qr\">запрещенной социальной сети</a>\n"
        "Подписывайтесь, чтобы занять место в первом ряду 🔜"
    )

    # Получаем file_id стартовой картинки
    # start_image_row = get_cinemalogy_material("cinemalogy_start_image")
    # start_image = start_image_row["telegram_file_id"]

    start_image = "AgACAgIAAxkBAAIH42qInJBlpoiQ4TMmvWsXi5T_mzlFAAIkIGsbEdFBSMYKNDSUr6KIAQADAgADeQADPQQ"

    # Отправляем фото + текст + кнопки ОДНИМ сообщением
    await message.answer_photo(
        photo=start_image,
        caption=start_text,
        # reply_markup=start_keyboard()
        reply_markup=start_keyboard_v2(),
        parse_mode="HTML"
    )
