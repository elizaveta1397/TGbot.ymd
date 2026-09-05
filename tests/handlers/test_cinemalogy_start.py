"""
Шаг 1. Старт Cinemalogy (handlers/cinemalogy/start.py).

Это самый первый экран воронки — именно здесь сидел баг #7
(опечатка в имени переменной ловилась только в проде).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.start import start_cinemalogy


def _callback_data(markup):
    return {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if button.callback_data
    }


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


async def test_regular_user_sees_closed_announcement_without_choose_frame_button(
    db, fake_message
):
    """
    Процесс сейчас закрыт для всех, кроме админа: обычный пользователь
    должен видеть только анонс, без кнопки "Выбрать кадр" — иначе он
    попадёт в воронку, хотя она не работает.
    """

    await start_cinemalogy(message=fake_message)

    kwargs = fake_message.answer_photo.await_args.kwargs
    assert "cinemalogy_choose_frame" not in _callback_data(kwargs["reply_markup"])
    assert "Синемалогию" in kwargs["caption"]


async def test_admin_sees_working_funnel_with_choose_frame_button(
    db, fake_message
):
    """
    Админ (владелец бота или admin_mode = "on") должен видеть рабочую
    воронку даже пока она закрыта для остальных — чтобы можно было
    её проверить.
    """

    set_parameter(fake_message.from_user.id, "admin_mode", "on")

    await start_cinemalogy(message=fake_message)

    kwargs = fake_message.answer_photo.await_args.kwargs
    assert "cinemalogy_choose_frame" in _callback_data(kwargs["reply_markup"])
    assert "Нажмите на кнопку «Выбрать кадр»" in kwargs["caption"]
