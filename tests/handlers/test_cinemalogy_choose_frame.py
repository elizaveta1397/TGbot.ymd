"""
Шаг 3. Выбор кадра (handlers/cinemalogy/choose_frame.py).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.choose_frame import choose_frame


async def test_choose_frame_first_visit_shows_frame_one(
    db, fake_callback, material
):
    material("cinemalogy_frame_01_image", telegram_file_id="FRAME_1")

    await choose_frame(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["photo"] == "FRAME_1"

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "current_step") == "choose_frame"
    assert get_parameter(telegram_id, "cinemalogy_current_frame") == "1"


async def test_choose_frame_repeat_visit_redirects_to_result(
    db, fake_callback, monkeypatch
):
    """
    Если пользователь уже выбирал кадр раньше (и не находится в
    admin_mode), должен сразу увидеть результат, а не кадр 1 заново.
    """

    telegram_id = fake_callback.from_user.id
    set_parameter(telegram_id, "cinemalogy_choice", "3")

    called_with = {}

    async def fake_result(callback):
        called_with["callback"] = callback

    monkeypatch.setattr(
        "handlers.cinemalogy.result.result", fake_result
    )

    await choose_frame(fake_callback)

    assert called_with.get("callback") is fake_callback
    fake_callback.message.answer_photo.assert_not_awaited()


async def test_choose_frame_admin_mode_shows_frame_one_even_with_prior_choice(
    db, fake_callback, material
):
    material("cinemalogy_frame_01_image", telegram_file_id="FRAME_1")

    telegram_id = fake_callback.from_user.id
    set_parameter(telegram_id, "cinemalogy_choice", "3")
    set_parameter(telegram_id, "admin_mode", "on")

    await choose_frame(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
