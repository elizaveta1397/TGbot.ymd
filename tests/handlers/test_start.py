"""
handlers/start.py — точка входа /start и кнопки главного меню.
"""

import sqlite3
from types import SimpleNamespace

from bot_services.database import add_user
from handlers.start import (
    about_me,
    cinemalogy_start,
    lullabies,
    start_handler,
)


def _command(args=None):
    return SimpleNamespace(args=args)


def _event_types(db, telegram_id):
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT event_type FROM user_events WHERE telegram_id = ?",
        (telegram_id,),
    )
    rows = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rows


async def test_start_handler_registers_new_user_and_notifies_admin(
    db, fake_message
):
    await start_handler(fake_message, _command())

    user = db.get_user(fake_message.from_user.id)
    assert user is not None

    fake_message.bot.send_message.assert_awaited_once()  # notify_new_user


async def test_start_handler_default_reply_for_new_user(db, fake_message):
    await start_handler(fake_message, _command())

    fake_message.answer.assert_awaited_once()
    args, kwargs = fake_message.answer.await_args
    assert args[0] == "Добро пожаловать"
    assert kwargs["reply_markup"] is not None


async def test_start_handler_does_not_reregister_existing_user(db, fake_message):
    add_user(
        telegram_id=fake_message.from_user.id,
        username="testuser",
        first_name="Test",
        last_name=None,
    )

    await start_handler(fake_message, _command())

    fake_message.bot.send_message.assert_not_awaited()  # notify_new_user не должен звать
    fake_message.answer.assert_awaited_once()


async def test_start_handler_cinemalogy_deep_link_routes_to_cinemalogy(
    db, fake_message, material
):
    material("cinemalogy_start_image", telegram_file_id="IMG")  # на случай будущего чтения из БД

    await start_handler(fake_message, _command(args="cinemalogy_promo"))

    # Экран приветствия /start вообще не должен уйти —
    # вместо него должен открыться экран Cinemalogy
    from bot_services.user_parameters import get_parameter

    assert get_parameter(
        fake_message.from_user.id, "current_step"
    ) == "cinemalogy_start"


async def test_about_me_button_sends_link(db, fake_message):
    await about_me(fake_message)

    fake_message.answer.assert_awaited_once()
    assert "telegra.ph" in fake_message.answer.await_args.args[0]


async def test_about_me_button_logs_analytics_and_current_step(db, fake_message):
    from bot_services.user_parameters import get_parameter

    telegram_id = fake_message.from_user.id

    await about_me(fake_message)

    assert get_parameter(telegram_id, "current_step") == "menu_about_me"

    events = _event_types(db, telegram_id)
    assert events == ["menu_about_me"]


async def test_lullabies_button_sends_link(db, fake_message):
    await lullabies(fake_message)

    fake_message.answer.assert_awaited_once()
    assert "t.me" in fake_message.answer.await_args.args[0]


async def test_lullabies_button_logs_analytics_and_current_step(db, fake_message):
    from bot_services.user_parameters import get_parameter

    telegram_id = fake_message.from_user.id

    await lullabies(fake_message)

    assert get_parameter(telegram_id, "current_step") == "menu_lullabies"

    events = _event_types(db, telegram_id)
    assert events == ["menu_lullabies"]


async def test_cinemalogy_menu_button_opens_cinemalogy(db, fake_message):
    await cinemalogy_start(fake_message)

    fake_message.answer_photo.assert_awaited_once()
