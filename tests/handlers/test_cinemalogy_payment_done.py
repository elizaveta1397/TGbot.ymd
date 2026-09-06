"""
Шаг 10. Экран после подтверждения оплаты (handlers/cinemalogy/payment_done.py).
"""

import sqlite3

from bot_services.user_parameters import get_parameter, set_parameter
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


async def test_payment_done_saves_current_step(db, fake_callback):
    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "mini")

    await payment_done(fake_callback)

    assert get_parameter(
        fake_callback.from_user.id, "current_step"
    ) == "payment_done"


async def test_payment_done_logs_analytics_event_with_tariff(db, fake_callback):
    """
    Раньше этот шаг вообще не писал аналитику — самый важный шаг
    воронки (подтверждение оплаты) не попадал в user_events.
    """

    set_parameter(fake_callback.from_user.id, "cinemalogy_tariff", "maxi")

    await payment_done(fake_callback)

    conn = sqlite3.connect(db.DB_PATH)
    rows = conn.execute(
        "SELECT event_type, event_data FROM user_events"
    ).fetchall()
    conn.close()

    assert ("cinemalogy_payment_done", "maxi") in rows
