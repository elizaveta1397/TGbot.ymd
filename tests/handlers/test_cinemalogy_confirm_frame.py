"""
Шаг 4. Подтверждение выбора кадра (handlers/cinemalogy/confirm_frame.py).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.confirm_frame import back_to_frames, frame_select


async def test_frame_select_sends_confirmation_animation_with_movie_title(
    db, fake_callback, material
):
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "3")
    material("cinemalogy_frame_03_confirm_gif", telegram_file_id="GIF_3")
    material("cinemalogy_frame_03_movie_title", text="Пролетая над гнездом кукушки")

    await frame_select(fake_callback)

    fake_callback.message.answer_animation.assert_awaited_once()
    kwargs = fake_callback.message.answer_animation.await_args.kwargs
    assert kwargs["animation"] == "GIF_3"
    assert "Пролетая над гнездом кукушки" in kwargs["caption"]

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "current_step") == "confirm_frame"


async def test_frame_select_survives_missing_movie_title(db, fake_callback):
    """
    Материалов для кадра может ещё не быть в БД — экран не должен падать,
    просто название фильма будет пустым.
    """

    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "7")

    await frame_select(fake_callback)

    fake_callback.message.answer_animation.assert_awaited_once()


async def test_back_to_frames_shows_same_frame_again(db, fake_callback, material):
    material("cinemalogy_frame_05_image", telegram_file_id="FRAME_5")
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "5")

    await back_to_frames(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    assert (
        fake_callback.message.answer_photo.await_args.kwargs["photo"] == "FRAME_5"
    )
