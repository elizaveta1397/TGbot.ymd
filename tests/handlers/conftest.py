"""
Общие фикстуры для тестов хендлеров.

Хендлеры вызываются напрямую (без Dispatcher/Bot) с "фейковыми"
Message/CallbackQuery — простыми моками с нужными атрибутами и
async-методами. Это не полноценная симуляция aiogram, зато дёшево и
достаточно, чтобы поймать главное: упал хендлер необработанным
исключением или нет, и что именно он отправил пользователю.
"""

import sqlite3
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def fake_user():
    return SimpleNamespace(
        id=100500,
        username="testuser",
        first_name="Test",
        last_name=None,
        language_code="ru",
    )


@pytest.fixture
def fake_message(fake_user):
    """
    Фейковое Message: все методы отправки/редактирования — AsyncMock,
    чтобы можно было проверить и что было вызвано, и с какими
    аргументами.
    """

    message = MagicMock()
    message.from_user = fake_user
    message.bot = AsyncMock()

    message.answer = AsyncMock()
    message.answer_photo = AsyncMock()
    message.answer_animation = AsyncMock()
    message.answer_document = AsyncMock()
    message.delete = AsyncMock()
    message.edit_media = AsyncMock()

    # reply_markup.inline_keyboard читается в frame_navigation при
    # пересборке клавиатуры поверх текущей
    message.reply_markup = SimpleNamespace(inline_keyboard=[])

    return message


@pytest.fixture
def fake_callback(fake_user, fake_message):
    callback = MagicMock()
    callback.from_user = fake_user
    callback.message = fake_message
    callback.bot = AsyncMock()
    callback.answer = AsyncMock()
    callback.data = None
    return callback


def insert_material(
    db,
    code,
    *,
    type="photo",
    telegram_file_id="FILE_ID",
    text=None,
    url=None,
    is_active=1,
):
    """
    Кладёт одну строку в materials_cinemalogy — тем хендлерам, что
    читают материалы через get_material(), нужны реальные данные в БД.
    """

    conn = sqlite3.connect(db.DB_PATH)
    conn.execute(
        """
        INSERT INTO materials_cinemalogy
            (code, type, telegram_file_id, text, url, is_active)
        VALUES (:code, :type, :telegram_file_id, :text, :url, :is_active)
        """,
        {
            "code": code,
            "type": type,
            "telegram_file_id": telegram_file_id,
            "text": text,
            "url": url,
            "is_active": is_active,
        },
    )
    conn.commit()
    conn.close()


@pytest.fixture
def material(db):
    """
    Фабрика материалов: material(code, text="...", url="...", ...)
    """

    def _make(code, **kwargs):
        insert_material(db, code, **kwargs)

    return _make
