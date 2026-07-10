"""
Шаг 6. Приглашение на кинопоказ.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.invitation import invitation_keyboard

from services.database import add_event
from services.user_parameters import set_parameter

router = Router()


@router.callback_query(F.data == "cinemalogy_invitation")
async def invitation(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    set_parameter(
        telegram_id,
        "current_step",
        "invitation"
    )

    add_event(
        telegram_id,
        "cinemalogy_invitation"
    )

    # --- единственное добавление: загрузка материалов из таблицы ---
    from services.cinemalogy.materials import get_material

    image_row = get_material("cinemalogy_invitation_image")
    text_row = get_material("cinemalogy_invitation_text")

    # ---------------------------------------------------------------

    await callback.message.answer_photo(
        photo=image_row["telegram_file_id"],
        caption=text_row["text"],
        reply_markup=invitation_keyboard()
    )

    await callback.answer()
