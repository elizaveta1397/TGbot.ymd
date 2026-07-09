from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from services.database import (
    get_user,
    add_user,
    update_last_activity,
    add_event
)

from keyboards.main_menu import main_menu
from services.admin_notifications import notify_new_user

router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
    command: CommandObject
):

    telegram_user = message.from_user

    # deep link (/start payload)
    source = command.args

    print(f"DEEP LINK = {source}")

    # ----------------------------
    # CINEMALOGY ROUTING
    # ----------------------------
    if source and source.startswith("cinemalogy"):

        from handlers.cinemalogy.start import start_cinemalogy

        await start_cinemalogy(
            message=message,
            source=source
        )
        return

    # ----------------------------
    # USER LOGIC
    # ----------------------------
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

        update_last_activity(telegram_user.id)

        add_event(
            telegram_user.id,
            "start",
            source
        )

    # ----------------------------
    # DEFAULT RESPONSE
    # ----------------------------
    await message.answer(
        "Добро пожаловать",
        reply_markup=main_menu
    )

from aiogram import F

@router.message(F.photo)
async def get_file_id(message: Message):
    await message.answer(message.photo[-1].file_id)

@router.message(F.animation)
async def get_gif_id(message: Message):
    await message.answer(message.animation.file_id)
