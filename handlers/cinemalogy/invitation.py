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

    await callback.message.answer_photo(
        photo="[INVITATION_IMAGE]",
        caption="[INVITATION_TEXT]",
        reply_markup=invitation_keyboard()
    )

    await callback.answer()
