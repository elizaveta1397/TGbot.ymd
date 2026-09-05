"""
Шаг 6. Приглашение на кинопоказ (handlers/cinemalogy/invitation.py).
"""

from bot_services.user_parameters import get_parameter
from handlers.cinemalogy.invitation import invitation


async def test_invitation_sends_photo(db, fake_callback, material):
    material("cinemalogy_invitation_image", telegram_file_id="INVITE_IMG")

    await invitation(fake_callback)

    fake_callback.message.answer_photo.assert_awaited_once()
    kwargs = fake_callback.message.answer_photo.await_args.kwargs
    assert kwargs["photo"] == "INVITE_IMG"

    telegram_id = fake_callback.from_user.id
    assert get_parameter(telegram_id, "current_step") == "invitation"
