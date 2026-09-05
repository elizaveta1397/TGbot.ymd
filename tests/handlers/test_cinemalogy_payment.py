"""
Шаг 8. Оплата (handlers/cinemalogy/payment.py).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.payment import payment, payment_back


async def test_payment_shows_price_for_selected_tariff(db, fake_callback):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "midi")

    await payment(fake_callback)

    fake_callback.message.answer.assert_awaited_once()
    text = fake_callback.message.answer.await_args.args[0]
    assert "4000 рублей" in text
    assert "Midi" in text

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "current_step") == "payment"


async def test_payment_notifies_admin_of_payment_start(db, fake_callback):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "mini")

    await payment(fake_callback)

    fake_callback.bot.send_message.assert_awaited_once()


async def test_payment_back_reopens_tariff_screen(db, fake_callback, material):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "maxi")
    material("ticket_maxi_image", telegram_file_id="TICKET_MAXI")
    material("ticket_maxi_text", text="Макси-билет")

    await payment_back(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    assert (
        fake_callback.message.answer_photo.await_args.kwargs["photo"]
        == "TICKET_MAXI"
    )
