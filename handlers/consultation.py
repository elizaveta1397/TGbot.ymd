from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.consultation_keyboard import consultation_keyboard
from bot_services.admin_notifications import notify_admin_consultation_request

router = Router()


@router.callback_query(lambda c: c.data == "consultation_start")
async def consultation_start(callback: CallbackQuery):

    user = callback.from_user

    text = (
        "К сожалению, на данный момент окна для записи в личную терапию "
        "с Елизаветой отсутствуют.\n\n"
        "Для записи в лист ожидания нажмите кнопку 👇🏼"
    )

    await callback.message.answer(
        text,
        reply_markup=consultation_keyboard()
    )

    # отправляем админу уведомление
    await notify_admin_consultation_request(
        callback.bot,
        user
    )

    await callback.answer()
