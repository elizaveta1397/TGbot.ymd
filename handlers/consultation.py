# handlers/consultation.py

from aiogram import Router
from aiogram.types import CallbackQuery, Message, User
from aiogram import Bot

from keyboards.consultation_keyboard import consultation_keyboard
from bot_services.admin_notifications import notify_admin_consultation_request
from bot_services.database import add_event
from bot_services.user_parameters import set_parameter

router = Router()


async def send_consultation_waitlist(
    message: Message,
    user: User,
    bot: Bot
):
    """
    Общая точка для обоих входов в запись на консультацию — кнопка
    главного меню (handlers/start.py::sign_up) и инлайн-кнопка
    "consultation_start" со стартового экрана Cinemalogy
    (consultation_start ниже). Аналитика и current_step пишутся тут
    один раз — покрывают оба входа.
    """

    set_parameter(user.id, "current_step", "consultation_waitlist")

    add_event(
        user.id,
        "consultation_request",
        None
    )

    text = (
        "К сожалению, на данный момент окна для записи в личную терапию "
        "с Елизаветой отсутствуют.\n\n"
        "Для записи в лист ожидания нажмите кнопку 👇🏼"
    )

    await message.answer(
        text,
        reply_markup=consultation_keyboard()
    )

    # отправляем админу уведомление
    await notify_admin_consultation_request(
        bot,
        user
    )


@router.callback_query(lambda c: c.data == "consultation_start")
async def consultation_start(callback: CallbackQuery):

    await send_consultation_waitlist(
        message=callback.message,
        user=callback.from_user,
        bot=callback.bot
    )

    await callback.answer()
