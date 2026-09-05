"""
Шаг 10. Экран после подтверждения оплаты (handlers/cinemalogy/payment_done.py).
"""

from bot_services.user_parameters import set_parameter
from handlers.cinemalogy.payment_done import payment_done


async def test_payment_done_thanks_user_and_shows_main_menu(db, fake_callback):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "mini")

    await payment_done(fake_callback)

    fake_callback.message.answer.assert_awaited_once()
    kwargs = fake_callback.message.answer.await_args.kwargs
    assert kwargs["reply_markup"] is not None


async def test_payment_done_notifies_admin_with_tariff(db, fake_callback):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "midi")

    await payment_done(fake_callback)

    fake_callback.bot.send_message.assert_awaited_once()
    args = fake_callback.bot.send_message.await_args.args
    assert "midi" in args[1]

    # payment_done — единственное "неглухое" уведомление (см. CLAUDE.md)
    kwargs = fake_callback.bot.send_message.await_args.kwargs
    assert "disable_notification" not in kwargs
