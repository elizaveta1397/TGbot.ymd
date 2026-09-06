"""
Шаг 5. Результат выбора кадра (handlers/cinemalogy/result.py).
"""

from bot_services.user_parameters import get_parameter, set_parameter
from handlers.cinemalogy.result import result


async def test_result_sends_photo_with_material_text(db, fake_callback, material):
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "2")
    material("cinemalogy_frame_02_image", telegram_file_id="FRAME_2")
    material("cinemalogy_frame_02_result_text", text="Про этот фильм думают многие")

    await result(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["photo"] == "FRAME_2"
    assert kwargs["caption"] == "Про этот фильм думают многие"

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "cinemalogy_choice") == "2"
    assert get_parameter(telegram_id, "current_step") == "result"


async def test_result_falls_back_to_default_text_when_material_missing(
    db, fake_callback, material
):
    set_parameter(fake_callback.from_user.id, "cinemalogy_current_frame", "9")
    material("cinemalogy_frame_09_image", telegram_file_id="FRAME_9")
    # текст результата для кадра 9 сознательно не создаём

    await result(fake_callback)

    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["caption"] == "Ваш выбор сохранён."
