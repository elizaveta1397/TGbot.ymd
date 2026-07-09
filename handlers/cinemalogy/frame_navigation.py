"""
Навигация по кадрам Cinemalogy.
"""

from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup

from services.user_parameters import (
    get_parameter,
    set_parameter
)

from services.cinemalogy.materials import get_material

router = Router()


CAPTION_TEXT = (
    "Внимательно посмотрите на кадры из фильмов. Не оценивайте их критически\n\n"
    "Выберите тот, который первым вызвал наиболее сильный эмоциональный отклик"
)


@router.callback_query(
    lambda c: c.data in (
        "frame_next",
        "frame_prev",
        "frame_select"
    )
)
async def frame_navigation(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    current_frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    if not current_frame:
        current_frame = "1"

    current_frame = int(current_frame)

    #
    # Следующий кадр (вперёд)
    #
    if callback.data == "frame_next":

        if current_frame < 12:
            current_frame += 1
        else:
            current_frame = 1   # кольцевая навигация

        set_parameter(
            telegram_id,
            "cinemalogy_current_frame",
            str(current_frame)
        )

        image = get_material(
            f"cinemalogy_frame_{current_frame:02d}_image"
        )

        new_keyboard = InlineKeyboardMarkup(
            inline_keyboard=callback.message.reply_markup.inline_keyboard
        )

        await callback.message.edit_media(
            InputMediaPhoto(
                media=image["telegram_file_id"],
                caption=CAPTION_TEXT
            ),
            reply_markup=new_keyboard
        )

        await callback.answer()
        return

    #
    # Предыдущий кадр (назад)
    #
    if callback.data == "frame_prev":

        if current_frame > 1:
            current_frame -= 1
        else:
            current_frame = 12  # кольцевая навигация

        set_parameter(
            telegram_id,
            "cinemalogy_current_frame",
            str(current_frame)
        )

        image = get_material(
            f"cinemalogy_frame_{current_frame:02d}_image"
        )

        new_keyboard = InlineKeyboardMarkup(
            inline_keyboard=callback.message.reply_markup.inline_keyboard
        )

        await callback.message.edit_media(
            InputMediaPhoto(
                media=image["telegram_file_id"],
                caption=CAPTION_TEXT
            ),
            reply_markup=new_keyboard
        )

        await callback.answer()
        return

    #
    # Выбран кадр
    #
    if callback.data == "frame_select":
        await callback.answer()
