"""
middlewares/activity.py — запись события "message" в user_events.

Баг из CLAUDE.md: hasattr(event, "text") истинно для ЛЮБОГО Message
(поле есть всегда, просто None для медиа) — событие "message" писалось
и для фото/стикеров с event_data=None. Правка — проверять сам текст
(getattr(..., None) + truthiness), а не наличие атрибута.
"""

import sqlite3
from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot_services.database import add_user
from middlewares.activity import ActivityMiddleware


def fake_event(*, text=None, has_text_attr=True):
    user = SimpleNamespace(id=100500, username="testuser")

    if has_text_attr:
        return SimpleNamespace(from_user=user, text=text)

    # CallbackQuery в реальном aiogram не имеет поля "text" вовсе.
    return SimpleNamespace(from_user=user)


async def call_middleware(event):
    middleware = ActivityMiddleware()
    handler = AsyncMock(return_value="handled")

    result = await middleware(handler, event, {})

    handler.assert_awaited_once_with(event, {})
    return result


def get_events(db, telegram_id):
    conn = sqlite3.connect(db.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event_type, event_data FROM user_events WHERE telegram_id = ?",
        (telegram_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


async def test_text_message_logs_message_event(db):
    add_user(100500, "testuser", "Test", None)

    await call_middleware(fake_event(text="привет"))

    rows = get_events(db, 100500)
    assert len(rows) == 1
    assert rows[0]["event_type"] == "message"
    assert rows[0]["event_data"] == "привет"


async def test_media_message_does_not_log_message_event(db):
    """
    Фото/стикер/войс и т.п.: text=None, но атрибут "text" присутствует
    (как у настоящего aiogram Message) — до фикса это всё равно писало
    "message" с event_data=None.
    """

    add_user(100500, "testuser", "Test", None)

    await call_middleware(fake_event(text=None))

    assert get_events(db, 100500) == []


async def test_callback_query_without_text_attr_does_not_crash_or_log(db):
    add_user(100500, "testuser", "Test", None)

    await call_middleware(fake_event(has_text_attr=False))

    assert get_events(db, 100500) == []
