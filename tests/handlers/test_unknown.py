"""
handlers/unknown.py — фолбэк на нераспознанное сообщение.
"""

from types import SimpleNamespace

from bot_services.database import set_user_parameter
from handlers.unknown import process_unknown, process_unknown_media


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


async def test_unknown_media_regular_user_gets_help_reply_and_notifies_care_team(
    db, fake_message
):
    """
    Обычный пользователь прислал войс (не текст) — тот же сценарий
    unknown, что и для текста, а не тишина/падение.
    """

    fake_message.text = None
    fake_message.content_type = "voice"

    await process_unknown_media(fake_message)

    fake_message.answer.assert_awaited_once()
    assert "меню" in fake_message.answer.await_args.args[0]

    fake_message.bot.send_message.assert_awaited_once()  # notify_care_team
    kwargs = fake_message.bot.send_message.await_args.kwargs
    assert "voice" in kwargs["text"]


async def test_unknown_media_admin_gets_photo_file_id(db, fake_message):
    """
    В admin_mode медиа не уходит в unknown-сценарий — админу
    возвращается file_id вложения (тут — самое крупное фото).
    """

    telegram_id = fake_message.from_user.id
    set_user_parameter(telegram_id, "admin_mode", "on")

    fake_message.text = None
    fake_message.content_type = "photo"
    fake_message.photo = [
        SimpleNamespace(file_id="SMALL"),
        SimpleNamespace(file_id="LARGE"),
    ]

    await process_unknown_media(fake_message)

    fake_message.answer.assert_awaited_once_with("file_id: LARGE")
    fake_message.bot.send_message.assert_not_awaited()  # не unknown-сценарий


async def test_unknown_media_admin_gets_video_note_file_id(db, fake_message):
    """Кружки (video_note) — тот же путь, что фото, другой атрибут."""

    telegram_id = fake_message.from_user.id
    set_user_parameter(telegram_id, "admin_mode", "on")

    fake_message.text = None
    fake_message.content_type = "video_note"
    fake_message.video_note = SimpleNamespace(file_id="CIRCLE")

    await process_unknown_media(fake_message)

    fake_message.answer.assert_awaited_once_with("file_id: CIRCLE")


async def test_unknown_media_admin_unknown_content_type_reports_no_file_id(
    db, fake_message
):
    """content_type без file_id (например, location) — не падаем."""

    telegram_id = fake_message.from_user.id
    set_user_parameter(telegram_id, "admin_mode", "on")

    fake_message.text = None
    fake_message.content_type = "location"

    await process_unknown_media(fake_message)

    fake_message.answer.assert_awaited_once()
    assert "Не нашёл file_id" in fake_message.answer.await_args.args[0]
