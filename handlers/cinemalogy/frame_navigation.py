"""
Навигация по кадрам Cinemalogy.
"""

from aiogram import Router
from aiogram.types import CallbackQuery, InputMediaPhoto

from services.user_parameters import (
    get_parameter,
    set_parameter
)

from services.cinemalogy.materials import get_material

router = Router()


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

        text = get_material(
            f"cinemalogy_frame_{current_frame:02d}_text"
        )

        await callback.message.edit_media(
            InputMediaPhoto(
                media=image["telegram_file_id"],
                caption=text["text"] if text else ""
            ),
            reply_markup=callback.message.reply_markup
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

        text = get_material(
            f"cinemalogy_frame_{current_frame:02d}_text"
        )

        await callback.message.edit_media(
            InputMediaPhoto(
                media=image["telegram_file_id"],
                caption=text["text"] if text else ""
            ),
            reply_markup=callback.message.reply_markup
        )

        await callback.answer()
        return

    #
    # Выбран кадр
    #
    if callback.data == "frame_select":
        await callback.answer()

