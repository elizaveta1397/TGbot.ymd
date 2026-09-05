"""
Шаг 1. Старт Cinemalogy (handlers/cinemalogy/start.py).

Это самый первый экран воронки — именно здесь сидел баг #7
(опечатка в имени переменной ловилась только в проде).
"""

from bot_services.user_parameters import get_parameter
from handlers.cinemalogy.start import start_cinemalogy


async def test_start_cinemalogy_sends_photo_with_keyboard(db, fake_message):
    await start_cinemalogy(message=fake_message, source="cinemalogy_ads")

    fake_message.answer_photo.assert_awaited_once()
    kwargs = fake_message.answer_photo.await_args.kwargs

    assert kwargs["photo"]  # непустой file_id, а не None/пусто
    assert kwargs["reply_markup"] is not None


async def test_start_cinemalogy_saves_current_step(db, fake_message):
    await start_cinemalogy(message=fake_message, source="cinemalogy_ads")

    telegram_id = fake_message.from_user.id
    assert get_parameter(telegram_id, "current_step") == "cinemalogy_start"


async def test_start_cinemalogy_uses_explicit_telegram_id_over_message_user(
    db, fake_message
):
    """
    Вызов из cinemalogy_home (callback от кнопки бота) должен считать
    telegram_id явным аргументом, а не message.from_user.id (иначе это
    будет id бота, см. докстринг start_cinemalogy).
    """

    other_id = 999

    await start_cinemalogy(message=fake_message, telegram_id=other_id)

    assert get_parameter(other_id, "current_step") == "cinemalogy_start"
    assert get_parameter(fake_message.from_user.id, "current_step") is None
