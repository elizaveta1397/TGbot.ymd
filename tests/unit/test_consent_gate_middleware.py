"""
middlewares/consent_gate.py — блокирует любое действие в боте для
пользователя, у которого нет строки в users (ещё не нажал
«Согласен(на)» на экране согласия). См. docs/IDEAS.md, п.1.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

from bot_services.database import add_user
from middlewares.consent_gate import ConsentGateMiddleware, NOT_CONSENTED_TEXT


def fake_event(*, text=None, data=None, has_text_attr=True, has_data_attr=True):
    user = SimpleNamespace(id=100500, username="testuser")

    kwargs = {"from_user": user, "answer": AsyncMock()}
    if has_text_attr:
        kwargs["text"] = text
    if has_data_attr:
        kwargs["data"] = data

    return SimpleNamespace(**kwargs)


async def call_middleware(event):
    middleware = ConsentGateMiddleware()
    handler = AsyncMock(return_value="handled")

    result = await middleware(handler, event, {})

    return handler, result


async def test_blocks_message_for_unregistered_user(db):
    event = fake_event(text="Обо мне")

    handler, result = await call_middleware(event)

    handler.assert_not_awaited()
    event.answer.assert_awaited_once_with(NOT_CONSENTED_TEXT)
    assert result is None


async def test_allows_message_for_registered_user(db):
    add_user(100500, "testuser", "Test", None)

    event = fake_event(text="Обо мне")
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})
    event.answer.assert_not_awaited()
    assert result == "handled"


async def test_start_command_always_allowed(db):
    event = fake_event(text="/start")
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})


async def test_start_with_deep_link_args_still_allowed(db):
    event = fake_event(text="/start cinemalogy_promo")
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})


async def test_policy_command_always_allowed(db):
    event = fake_event(text="/policy")
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})


async def test_consent_accept_callback_always_allowed(db):
    event = fake_event(data="consent_accept", has_text_attr=False)
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})


async def test_policy_view_callback_always_allowed(db):
    event = fake_event(data="policy_view", has_text_attr=False)
    handler, result = await call_middleware(event)

    handler.assert_awaited_once_with(event, {})


async def test_blocks_other_callback_for_unregistered_user(db):
    event = fake_event(data="delete_me_confirm", has_text_attr=False)

    handler, result = await call_middleware(event)

    handler.assert_not_awaited()
    event.answer.assert_awaited_once_with(NOT_CONSENTED_TEXT)


async def test_does_not_crash_without_from_user():
    event = SimpleNamespace(from_user=None, answer=AsyncMock())
    middleware = ConsentGateMiddleware()
    handler = AsyncMock(return_value="handled")

    result = await middleware(handler, event, {})

    handler.assert_awaited_once_with(event, {})
    assert result == "handled"
