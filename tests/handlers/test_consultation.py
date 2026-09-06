"""
handlers/consultation.py — запись в лист ожидания на консультацию.
"""

import sqlite3

from bot_services.user_parameters import get_parameter
from handlers.consultation import consultation_start, send_consultation_waitlist


async def test_send_consultation_waitlist_replies_and_notifies_admin(
    db, fake_message
):
    await send_consultation_waitlist(
        message=fake_message,
        user=fake_message.from_user,
        bot=fake_message.bot,
    )

    fake_message.answer.assert_awaited_once()
    assert "лист ожидания" in fake_message.answer.await_args.args[0]

    fake_message.bot.send_message.assert_awaited_once()


async def test_send_consultation_waitlist_logs_analytics_and_current_step(
    db, fake_message
):
    telegram_id = fake_message.from_user.id

    await send_consultation_waitlist(
        message=fake_message,
        user=fake_message.from_user,
        bot=fake_message.bot,
    )

    assert get_parameter(telegram_id, "current_step") == "consultation_waitlist"

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event_type FROM user_events WHERE telegram_id = ?",
        (telegram_id,),
    )
    events = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert events == ["consultation_request"]


async def test_consultation_start_callback_delegates_to_waitlist(
    db, fake_callback
):
    await consultation_start(fake_callback)

    fake_callback.message.answer.assert_awaited_once()
    fake_callback.answer.assert_awaited_once()
