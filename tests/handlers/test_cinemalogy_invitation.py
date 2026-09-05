"""
Шаг 6. Приглашение на кинопоказ (handlers/cinemalogy/invitation.py).
"""

from bot_services.user_parameters import get_parameter
from handlers.cinemalogy.invitation import invitation


def _callback_data(markup):
    return {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if button.callback_data
    }


async def test_invitation_sends_photo(db, fake_callback, material):
    material("cinemalogy_invitation_image", telegram_file_id="INVITE_IMG")

    await invitation(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["photo"] == "INVITE_IMG"

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "current_step") == "invitation"


async def test_invitation_hides_partners_button_when_no_active_partners(
    db, fake_callback, material
):
    material("cinemalogy_invitation_image", telegram_file_id="INVITE_IMG")
    # ни одного cinemalogy_partners_image_* не заведено

    await invitation(fake_callback)

    keyboard = fake_callback.message.answer_photo.await_args.kwargs["reply_markup"]
    assert "partners" not in _callback_data(keyboard)


async def test_invitation_shows_partners_button_when_active_partners_exist(
    db, fake_callback, material
):
    material("cinemalogy_invitation_image", telegram_file_id="INVITE_IMG")
    material("cinemalogy_partners_image_01", telegram_file_id="PARTNER_1")

    await invitation(fake_callback)

    keyboard = fake_callback.message.answer_photo.await_args.kwargs["reply_markup"]
    assert "partners" in _callback_data(keyboard)
