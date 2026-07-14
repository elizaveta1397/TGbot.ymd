"""
Шаг 6. Приглашение на кинопоказ.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.invitation import invitation_keyboard

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter
from bot_services.cinemalogy.materials import get_material

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

    # СНАЧАЛА УДАЛЯЕМ ТЕКУЩЕЕ СООБЩЕНИЕ
    try:
        await callback.message.delete()
    except Exception:
        pass

    image_row = get_material("cinemalogy_invitation_image")

    # ПОТОМ ОТПРАВЛЯЕМ НОВОЕ СООБЩЕНИЕ С ФОТО И КНОПКАМИ
    await callback.message.answer_photo(
        photo=image_row["telegram_file_id"],
        caption="Выберите ваш билет кнопкой ниже",
        reply_markup=invitation_keyboard()
    )

    await callback.answer()
