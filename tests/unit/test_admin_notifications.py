"""
Тесты для bot_services/admin_notifications.py.

По умолчанию все уведомления должны идти "тихо" (disable_notification=True),
кроме payment_done и запросов в отдел Заботы — это зафиксировано в
CLAUDE.md проекта, тесты не дают этому незаметно сломаться.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot_services.admin_notifications import (
    notify_admin_consultation_request,
    notify_admin_payment_done,
    notify_admin_payment_start,
    notify_admin_tariff_viewed,
    notify_care_team,
    notify_new_user,
)
from config import CARE_TEAM_CHAT_ID, NOTIFY_ADMIN_ID


@pytest.fixture
def bot():
    return AsyncMock()


@pytest.fixture
def user():
    return SimpleNamespace(
        id=42,
        username="liza",
        first_name="Liza",
        last_name=None,
        language_code="ru",
    )


async def test_notify_new_user_is_silent_and_goes_to_notify_admin(bot, user):
    await notify_new_user(bot, user, source="ads")

    bot.send_message.assert_awaited_once()
    kwargs = bot.send_message.await_args.kwargs

    assert kwargs["chat_id"] == NOTIFY_ADMIN_ID
    assert kwargs["disable_notification"] is True
    assert "42" in kwargs["text"]
    assert "ads" in kwargs["text"]


async def test_notify_new_user_handles_missing_optional_fields(bot):
    anon_user = SimpleNamespace(
        id=1, username=None, first_name="Anon", last_name=None, language_code=None
    )

    await notify_new_user(bot, anon_user, source=None)

    text = bot.send_message.await_args.kwargs["text"]
    assert "не указан" in text  # username/язык/источник — заглушки


async def test_notify_admin_payment_start_is_silent(bot, user):
    await notify_admin_payment_start(bot, user, tariff="VIP")

    args, kwargs = bot.send_message.await_args
    assert args[0] == NOTIFY_ADMIN_ID
    assert kwargs["disable_notification"] is True
    assert "VIP" in args[1]


async def test_notify_admin_payment_done_is_not_silent(bot, user):
    """
    payment_done — единственное исключение из "тихих" уведомлений
    (см. CLAUDE.md: silent-by-default кроме payment-done и care-team).
    """

    await notify_admin_payment_done(bot, user, tariff="VIP")

    args, kwargs = bot.send_message.await_args
    assert args[0] == NOTIFY_ADMIN_ID
    assert "disable_notification" not in kwargs


async def test_notify_admin_consultation_request_is_silent(bot, user):
    await notify_admin_consultation_request(bot, user)

    args, kwargs = bot.send_message.await_args
    assert args[0] == NOTIFY_ADMIN_ID
    assert kwargs["disable_notification"] is True


async def test_notify_admin_tariff_viewed_is_silent(bot, user):
    await notify_admin_tariff_viewed(bot, user, tariff_name="Standard")

    args, kwargs = bot.send_message.await_args
    assert args[0] == NOTIFY_ADMIN_ID
    assert kwargs["disable_notification"] is True
    assert "Standard" in args[1]


async def test_notify_care_team_goes_to_care_team_chat_and_is_not_silent(bot, user):
    await notify_care_team(bot, user, text="Помогите разобраться с тарифом")

    kwargs = bot.send_message.await_args.kwargs
    assert kwargs["chat_id"] == CARE_TEAM_CHAT_ID
    assert "disable_notification" not in kwargs
    assert "Помогите разобраться с тарифом" in kwargs["text"]
