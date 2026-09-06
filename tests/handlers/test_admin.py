"""
handlers/admin.py — панель администратора.

Отдельно проверяем build_admin_menu_text_and_keyboard() и
admin_username_input(): раньше они ходили в БД по захардкоженному
абсолютному пути (/home/botuser/telegram-bot/data/bot.db) вместо
database.DB_PATH — в тестах (и вообще при другой рабочей директории)
читали бы не свою, временную БД, а боевую. Теперь оба используют
database.DB_PATH, который патчит фикстура db.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot_services.database import add_user, set_user_parameter
from handlers.admin import (
    admin_entry,
    admin_grant,
    admin_revoke,
    admin_toggle,
    admin_username_input,
    awaiting_admin_username,
    build_admin_menu_text_and_keyboard,
    is_admin,
)


# ============================
# is_admin
# ============================

def test_is_admin_true_for_owner(db):
    assert is_admin(1) is True  # ADMIN_ID=1 в тестовом окружении (conftest)


def test_is_admin_true_when_admin_mode_on(db):
    set_user_parameter(100500, "admin_mode", "on")
    assert is_admin(100500) is True


def test_is_admin_false_otherwise(db):
    assert is_admin(100500) is False


# ============================
# admin_entry
# ============================

async def test_admin_entry_rejects_non_admin(db, fake_message):
    await admin_entry(fake_message)

    fake_message.answer.assert_awaited_once_with("Вы не админ.")


async def test_admin_entry_shows_menu_for_admin(db, fake_message):
    set_user_parameter(fake_message.from_user.id, "admin_mode", "on")

    await admin_entry(fake_message)

    fake_message.answer.assert_awaited_once()
    text = fake_message.answer.await_args.args[0]
    assert "Админ" in text
    assert str(fake_message.from_user.id) in text


# ============================
# build_admin_menu_text_and_keyboard — читает через database.DB_PATH
# ============================

async def test_build_admin_menu_lists_other_admins_from_configured_db(db):
    add_user(
        telegram_id=777,
        username="otheradmin",
        first_name="Other",
        last_name=None,
    )
    set_user_parameter(777, "admin_mode", "on")

    text, keyboard = await build_admin_menu_text_and_keyboard(100500)

    assert "@otheradmin (777)" in text
    assert "Ваш статус: off" in text
    assert keyboard.inline_keyboard  # клавиатура собралась


async def test_build_admin_menu_shows_no_other_admins_when_none(db):
    text, _ = await build_admin_menu_text_and_keyboard(1)

    assert "Нет других админов" in text


# ============================
# admin_toggle
# ============================

async def test_admin_toggle_turns_on_for_non_admin_yet(db, fake_callback):
    """
    is_admin() пропускает и не-админа: включение режима — это то,
    как обычный пользователь СТАНОВИТСЯ админом (ADMIN_ID уже админ
    всегда, остальным admin_mode выставляется вручную через grant —
    но сам toggle не проверяет права отдельно от is_admin()).
    """

    fake_callback.from_user.id = 1  # ADMIN_ID — единственный, кто сразу is_admin
    fake_callback.message.edit_text = AsyncMock()

    await admin_toggle(fake_callback)

    fake_callback.answer.assert_awaited_once_with("Статус обновлён")
    fake_callback.message.edit_text.assert_awaited_once()
    text = fake_callback.message.edit_text.await_args.args[0]
    assert "Ваш статус: on" in text


async def test_admin_toggle_turns_off_again(db, fake_callback):
    fake_callback.from_user.id = 1
    fake_callback.message.edit_text = AsyncMock()
    set_user_parameter(1, "admin_mode", "on")

    await admin_toggle(fake_callback)

    text = fake_callback.message.edit_text.await_args.args[0]
    assert "Ваш статус: off" in text


async def test_admin_toggle_rejects_non_admin(db, fake_callback):
    await admin_toggle(fake_callback)

    fake_callback.answer.assert_awaited_once_with("Вы не админ.")


# ============================
# admin_grant / admin_revoke
# ============================

async def test_admin_grant_prompts_for_username_and_sets_waiting_action(
    db, fake_callback
):
    fake_callback.from_user.id = 1

    await admin_grant(fake_callback)

    fake_callback.message.answer.assert_awaited_once()
    from bot_services.database import get_user_parameter
    assert get_user_parameter(1, "admin_waiting_action") == "grant"


async def test_admin_revoke_prompts_for_username_and_sets_waiting_action(
    db, fake_callback
):
    fake_callback.from_user.id = 1

    await admin_revoke(fake_callback)

    from bot_services.database import get_user_parameter
    assert get_user_parameter(1, "admin_waiting_action") == "revoke"


# ============================
# awaiting_admin_username
# ============================

async def test_awaiting_admin_username_false_for_non_admin(db):
    message = SimpleNamespace(from_user=SimpleNamespace(id=100500))

    assert await awaiting_admin_username(message) is False


# ============================
# admin_username_input — читает/пишет через database.DB_PATH
# ============================

async def test_admin_username_input_grant_sets_target_admin_mode_on(
    db, fake_message
):
    add_user(
        telegram_id=888,
        username="newadmin",
        first_name="New",
        last_name=None,
    )
    set_user_parameter(fake_message.from_user.id, "admin_waiting_action", "grant")
    fake_message.text = "@newadmin"

    await admin_username_input(fake_message)

    from bot_services.database import get_user_parameter
    assert get_user_parameter(888, "admin_mode") == "on"
    assert get_user_parameter(
        fake_message.from_user.id, "admin_waiting_action"
    ) is None


async def test_admin_username_input_revoke_clears_target_admin_mode(
    db, fake_message
):
    add_user(
        telegram_id=888,
        username="oldadmin",
        first_name="Old",
        last_name=None,
    )
    set_user_parameter(888, "admin_mode", "on")
    set_user_parameter(fake_message.from_user.id, "admin_waiting_action", "revoke")
    fake_message.text = "@oldadmin"

    await admin_username_input(fake_message)

    from bot_services.database import get_user_parameter
    assert get_user_parameter(888, "admin_mode") is None


async def test_admin_username_input_user_not_found(db, fake_message):
    set_user_parameter(fake_message.from_user.id, "admin_waiting_action", "grant")
    fake_message.text = "@ghost"

    await admin_username_input(fake_message)

    calls = [c.args[0] for c in fake_message.answer.await_args_list]
    assert any("не найден" in c for c in calls)
