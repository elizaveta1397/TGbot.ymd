"""
Шаг 3. Выбор кадра.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database import add_event
from services.user_parameters import (
    get_parameter,
    set_parameter
)

from keyboards.cinemalogy.frames import frame_keyboard
from handlers.cinemalogy.start import start_cinemalogy

router = Router()


CAPTION_TEXT = (
    "Внимательно посмотрите на кадры из фильмов. Не оценивайте их критически\n\n"
    "Выберите тот, который первым вызвал наиболее сильный эмоциональный отклик"
)


@router.callback_query(F.data == "cinemalogy_choose_frame")
async def choose_frame(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    # Запоминаем текущий шаг
    set_parameter(
        telegram_id,
        "current_step",
        "choose_frame"
    )

    # Аналитика
    add_event(
        telegram_id,
        "choose_frame"
    )

    # Проверяем, выбирал ли пользователь кадр ранее
    choice = get_parameter(
        telegram_id,
        "cinemalogy_choice"
    )

    admin_mode = get_parameter(
        telegram_id,
        "admin_mode"
    )

    if choice and admin_mode != "on":
        await callback.message.answer(
            "[STEP_5_RESULT]"
        )
        await callback.answer()
        return

    # Первый кадр
    set_parameter(
        telegram_id,
        "cinemalogy_current_frame",
        "1"
    )

    from services.cinemalogy.materials import get_material

    image = get_material("cinemalogy_frame_01_image")

    await callback.message.answer_photo(
        photo=image["telegram_file_id"],
        caption=CAPTION_TEXT,
        reply_markup=frame_keyboard()
    )

    await callback.answer()

@router.callback_query(F.data == "cinemalogy_home")
async def cinemalogy_home(callback: CallbackQuery):

    await start_cinemalogy(
        message=callback.message,
        source="home_button"
    )

    await callback.answer()
