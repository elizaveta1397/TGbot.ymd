"""
Шаг 8. Оплата.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.payment import payment_keyboard

from services.database import add_event
from services.user_parameters import set_parameter, get_parameter
from services.admin_notifications import notify_admin_payment_start

router = Router()


@router.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    tariff = get_parameter(
        telegram_id,
        "cinemalogy_tariff"
    )

    set_parameter(
        telegram_id,
        "current_step",
        "payment"
    )

    add_event(
        telegram_id,
        "cinemalogy_payment_opened",
        tariff
    )

    # уведомление админу
    await notify_admin_payment_start(
        callback.bot,
        callback.from_user,
        tariff
    )

    text = (
        "[PAYMENT_TEXT]\n\n"
        "Реквизиты: [CARD_DETAILS]\n"
        "Обязательно укажи @username в комментарии перевода."
    )

    await callback.message.answer(
        text,
        reply_markup=payment_keyboard()
    )

    await callback.answer()
