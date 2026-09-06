"""
handlers/start.py — точка входа /start, согласие на обработку ПДн
(152-ФЗ, см. docs/IDEAS.md п.1) и кнопки главного меню.
"""

import sqlite3
from types import SimpleNamespace

import pytest

from bot_services.database import add_user
from handlers.start import (
    _pending_sources,
    about_me,
    cinemalogy_start,
    consent_accept,
    lullabies,
    policy_command,
    policy_view,
    start_handler,
)


@pytest.fixture(autouse=True)
def _clean_pending_sources():
    # _pending_sources — модульный словарь (не БД), общий на все
    # тесты процесса; чистим, чтобы состояние одного теста не текло
    # в другой через общий fake_user.id.
    _pending_sources.clear()
    yield
    _pending_sources.clear()


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


async def test_start_handler_shows_consent_screen_for_new_user(
    db, fake_message
):
    await start_handler(fake_message, _command())

    # До согласия — не регистрируем и не уведомляем админа
    assert db.get_user(fake_message.from_user.id) is None
    fake_message.bot.send_message.assert_not_awaited()

    fake_message.answer.assert_awaited_once()
    args, kwargs = fake_message.answer.await_args
    assert "персональных данных" in args[0]
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
    assert fake_message.answer.await_args.args[0] == "Добро пожаловать"


async def test_start_handler_cinemalogy_deep_link_routes_existing_user(
    db, fake_message, material
):
    add_user(
        telegram_id=fake_message.from_user.id,
        username="testuser",
        first_name="Test",
        last_name=None,
    )
    material("cinemalogy_start_image", telegram_file_id="IMG")  # на случай будущего чтения из БД

    await start_handler(fake_message, _command(args="cinemalogy_promo"))

    from bot_services.user_parameters import get_parameter

    assert get_parameter(
        fake_message.from_user.id, "current_step"
    ) == "cinemalogy_start"


async def test_consent_accept_registers_user_and_notifies_admin(
    db, fake_message, fake_callback
):
    await start_handler(fake_message, _command(args="promo"))  # ставит consent-экран
    await consent_accept(fake_callback)

    user = db.get_user(fake_callback.from_user.id)
    assert user is not None
    assert user[-1] == "promo"  # колонка source — последняя в users

    fake_callback.bot.send_message.assert_awaited_once()  # notify_new_user

    events = _event_types(db, fake_callback.from_user.id)
    assert events == ["consent_given"]


async def test_consent_accept_shows_main_menu_by_default(
    db, fake_message, fake_callback
):
    # fake_callback.message — тот же объект, что и fake_message
    # (см. tests/handlers/conftest.py), поэтому .answer() ловит и
    # экран согласия (start_handler), и приветствие (consent_accept)
    await start_handler(fake_message, _command())
    await consent_accept(fake_callback)

    assert fake_message.answer.await_count == 2
    consent_call, welcome_call = fake_message.answer.await_args_list
    assert "персональных данных" in consent_call.args[0]
    assert welcome_call.args[0] == "Добро пожаловать"

    assert fake_callback.message.delete.await_count == 1


async def test_consent_accept_routes_to_cinemalogy_for_new_user(
    db, fake_message, fake_callback, material
):
    material("cinemalogy_start_image", telegram_file_id="IMG")

    await start_handler(fake_message, _command(args="cinemalogy_promo"))
    await consent_accept(fake_callback)

    from bot_services.user_parameters import get_parameter

    assert get_parameter(
        fake_callback.from_user.id, "current_step"
    ) == "cinemalogy_start"


async def test_policy_command_sends_document(fake_message):
    await policy_command(fake_message)

    fake_message.answer_document.assert_awaited_once()


async def test_policy_view_callback_sends_document(fake_callback):
    await policy_view(fake_callback)

    fake_callback.message.answer_document.assert_awaited_once()
    fake_callback.answer.assert_awaited_once()


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
