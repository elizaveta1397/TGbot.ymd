"""
Шаг 4. Подтверждение выбора кадра.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database import add_event
from services.user_parameters import (
    get_parameter,
    set_parameter
)

from keyboards.cinemalogy.frames import confirm_keyboard

router = Router()


@router.callback_query(F.data == "frame_select")
async def frame_select(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    current_frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    set_parameter(
        telegram_id,
        "current_step",
        "confirm_frame"
    )

    add_event(
        telegram_id,
        "confirm_frame",
        current_frame
    )

    from services.cinemalogy.materials import get_material

    gif = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_confirm_gif"
    )

    text = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_text"
    )

    await callback.message.answer_animation(
        animation=gif["telegram_file_id"] if gif and gif["telegram_file_id"] else None,
        caption=text["text"] if text else "",
        reply_markup=confirm_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_frames")
async def back_to_frames(callback: CallbackQuery):

    await callback.message.answer(
        "[STEP_3_FRAME]"
    )

    await callback.answer()
