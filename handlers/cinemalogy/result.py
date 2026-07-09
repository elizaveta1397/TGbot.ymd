"""
Шаг 5. Результат выбора кадра.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database import add_event
from services.user_parameters import (
    get_parameter,
    set_parameter,
    delete_parameter
)

from keyboards.cinemalogy.result import result_keyboard

router = Router()


@router.callback_query(F.data == "confirm_frame")
async def result(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    admin_mode = get_parameter(
        telegram_id,
        "admin_mode"
    )

    # Если включен режим администратора,
    # удаляем старый выбор
    if admin_mode == "on":
        delete_parameter(
            telegram_id,
            "cinemalogy_choice"
        )

    # Записываем окончательный выбор пользователя
    set_parameter(
        telegram_id,
        "cinemalogy_choice",
        frame
    )

    # Текущий шаг
    set_parameter(
        telegram_id,
        "current_step",
        "result"
    )

    # Аналитика
    add_event(
        telegram_id,
        "cinemalogy_result",
        frame
    )

    await callback.message.answer_photo(
        photo="[RESULT_IMAGE]",
        caption="[RESULT_TEXT]",
        reply_markup=result_keyboard()
    )

    await callback.answer()
