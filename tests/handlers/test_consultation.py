"""
handlers/consultation.py — запись в лист ожидания на консультацию.
"""

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


async def test_consultation_start_callback_delegates_to_waitlist(
    db, fake_callback
):
    await consultation_start(fake_callback)

    fake_callback.message.answer.assert_awaited_once()
    fake_callback.answer.assert_awaited_once()
