"""
Карусель партнёров (handlers/cinemalogy/partners.py).
"""

import pytest

from handlers.cinemalogy.partners import partners_next, partners_start


async def test_partners_start_shows_first_partner(db, fake_callback, material):
    material("cinemalogy_partners_image_01", telegram_file_id="PARTNER_1")
    material("cinemalogy_partners_image_02", telegram_file_id="PARTNER_2")

    await partners_start(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    assert fake_callback.message.answer_photo.await_args.args[0] == "PARTNER_1"


async def test_partners_next_wraps_around_to_first(db, fake_callback, material):
    material("cinemalogy_partners_image_01", telegram_file_id="PARTNER_1")
    material("cinemalogy_partners_image_02", telegram_file_id="PARTNER_2")
    fake_callback.data = "partners_next:1"  # уже на последнем (индекс 1 из 2)

    await partners_next(fake_callback)

    fake_callback.message.edit_media.assert_awaited_once()
    media = fake_callback.message.edit_media.await_args.kwargs["media"]
    assert media.media == "PARTNER_1"


async def test_partners_start_crashes_with_no_active_partners(db, fake_callback):
    """
    НАХОДКА, не тест-подтверждение желаемого поведения: если в
    materials_cinemalogy нет ни одного активного партнёра,
    partners_start падает необработанным IndexError вместо того,
    чтобы показать пользователю понятное сообщение. Тест фиксирует
    текущее (плохое) поведение — стоит завести отдельный фикс.
    """

    with pytest.raises(IndexError):
        await partners_start(fake_callback)
