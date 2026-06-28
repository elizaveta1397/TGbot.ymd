from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services.database import (
    get_user,
    add_user,
    update_last_activity
)

from keyboards.main_menu import main_menu

from services.database import add_event

from services.admin_notifications import notify_new_user

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    telegram_user = message.from_user

    parts = message.text.split(maxsplit=1)

    source = None

    if len(parts) > 1:
        source = parts[1]

    user = get_user(telegram_user.id)

    if user is None:

        add_user(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            source=source
        )

        await notify_new_user(
            message.bot,
            telegram_user,
            source
        )

    else:

        update_last_activity(
            telegram_user.id
        )

        add_event(
        telegram_user.id,
        "start",
        source
    )

    await message.answer(
    "Добро пожаловать",
    reply_markup=main_menu
)
