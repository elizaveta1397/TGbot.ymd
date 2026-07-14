"""
Шаг 8. Оплата.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.payment import payment_keyboard

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter, get_parameter

# импортируем существующую функцию показа тарифа
from handlers.cinemalogy.tariff import send_tariff

router = Router()


@router.callback_query(F.data == "payment")
async def payment(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    # удаляем предыдущий экран (тариф)
    try:
        await callback.message.delete()
    except:
        pass

    # читаем тариф, выбранный ранее
    tariff = get_parameter(telegram_id, "cinemalogy_tariff")

    # записываем шаг
    set_parameter(telegram_id, "current_step", "payment")

    # аналитика
    add_event(
        telegram_id,
        "cinemalogy_payment_opened",
        tariff
    )

    # стоимость
    prices = {
        "mini": "1000 рублей",
        "midi": "4000 рублей",
        "maxi": "9000 рублей"
    }

    price = prices.get(tariff, "—")

    text = (
        f"Забронированный билет:\n"
        f"Синемалогия — {tariff.capitalize()}\n\n"
        f"Оплатите {price} по реквизитам:\n"
        f"2202205004739089 (Сбер)\n"
        f"Елизавета Г.\n\n"
        f"Билет будет выслан в этот чат в течение суток с момента оплаты 🫶🏼\n\n"
        f"После оплаты нажмите, пожалуйста, на кнопку «Билет оплачен»"
    )

    await callback.message.answer(
        text,
        reply_markup=payment_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "payment_back")
async def payment_back(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    # удаляем экран оплаты
    try:
        await callback.message.delete()
    except:
        pass

    # читаем тариф
    tariff = get_parameter(telegram_id, "cinemalogy_tariff")

    # открываем экран выбранного тарифа
    await send_tariff(callback, tariff)

    await callback.answer()
