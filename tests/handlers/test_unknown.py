"""
handlers/unknown.py — фолбэк на нераспознанное сообщение.
"""

from handlers.unknown import process_unknown


async def test_unknown_message_gets_help_reply_and_notifies_care_team(
    db, fake_message
):
    fake_message.text = "почему бот не отвечает?????"

    await process_unknown(fake_message)

    fake_message.answer.assert_awaited_once()
    assert "меню" in fake_message.answer.await_args.args[0]

    fake_message.bot.send_message.assert_awaited_once()  # notify_care_team
    kwargs = fake_message.bot.send_message.await_args.kwargs
    assert "почему бот не отвечает?????" in kwargs["text"]


async def test_unknown_message_routes_admin_word_to_admin_entry(
    db, fake_message, monkeypatch
):
    fake_message.text = "админ"

    called_with = {}

    async def fake_admin_entry(message):
        called_with["message"] = message

    monkeypatch.setattr("handlers.admin.admin_entry", fake_admin_entry)

    await process_unknown(fake_message)

    assert called_with.get("message") is fake_message
    fake_message.answer.assert_not_awaited()
    fake_message.bot.send_message.assert_not_awaited()
