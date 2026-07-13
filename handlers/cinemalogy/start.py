"""
Старт процесса Cinemalogy.
"""

from aiogram import Router
from aiogram.types import Message

from keyboards.cinemalogy.start import start_keyboard

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter
from bot_services.cinemalogy.materials import get_material as get_cinemalogy_material  # ← добавлено

# Роутер нужен, чтобы __init__.py мог его импортировать
router = Router()


async def start_cinemalogy(
    message: Message,
    source: str | None = None
):
    """
    Первый экран Cinemalogy.
    """

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

    # Приветственный текст
    start_text = (
        "Добро пожаловать в мир синемалогии!\n\n"
        "Я – Гончарова Елизавета, EMDR-терапевт, интегративный психолог "
        "проведу вас в тайны вашего бессознательного через культовые фильмы."
    )

    # Получаем file_id из таблицы materials_cinemalogy
    start_image_row = get_cinemalogy_material("cinemalogy_start_image")
    start_image = start_image_row["telegram_file_id"]  # ← исправлено

    # Отправляем фото + текст + кнопки одним сообщением
    await message.answer_photo(
        photo=start_image,
        caption=start_text,
        reply_markup=start_keyboard()
    )

