"""
Навигация по кадрам (handlers/cinemalogy/frame_navigation.py).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.frame_navigation import frame_navigation


async def test_frame_next_advances_to_next_frame(db, fake_callback, material):
    material("cinemalogy_frame_02_image", telegram_file_id="FRAME_2")
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "1")
    fake_callback.data = "frame_next"

    await frame_navigation(fake_callback)

    assert get_parameter(
        fake_callback.from_user.id, "cinemalogy_current_frame"
    ) == "2"
    fake_callback.message.edit_media.assert_awaited_once()


async def test_frame_next_wraps_around_after_last_frame(
    db, fake_callback, material
):
    material("cinemalogy_frame_01_image", telegram_file_id="FRAME_1")
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "12")
    fake_callback.data = "frame_next"

    await frame_navigation(fake_callback)

    assert get_parameter(
        fake_callback.from_user.id, "cinemalogy_current_frame"
    ) == "1"


async def test_frame_prev_goes_back_one_frame(db, fake_callback, material):
    material("cinemalogy_frame_04_image", telegram_file_id="FRAME_4")
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "5")
    fake_callback.data = "frame_prev"

    await frame_navigation(fake_callback)

    assert get_parameter(
        fake_callback.from_user.id, "cinemalogy_current_frame"
    ) == "4"


async def test_frame_prev_wraps_around_before_first_frame(
    db, fake_callback, material
):
    material("cinemalogy_frame_12_image", telegram_file_id="FRAME_12")
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "1")
    fake_callback.data = "frame_prev"

    await frame_navigation(fake_callback)

    assert get_parameter(
        fake_callback.from_user.id, "cinemalogy_current_frame"
    ) == "12"
