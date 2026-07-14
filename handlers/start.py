from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

from bot_services.database import (
    get_user,
    add_user,
    update_last_activity,
    add_event
)

from keyboards.main_menu import main_menu
from bot_services.admin_notifications import notify_new_user

router = Router()


# ============================
# START HANDLER
# ============================
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


# ============================
# FILE ID HELPERS
# ============================
@router.message(F.photo)
async def get_file_id(message: Message):
    await message.answer(message.photo[-1].file_id)


@router.message(F.animation)
async def get_gif_id(message: Message):
    await message.answer(message.animation.file_id)


# ============================
# MAIN MENU BUTTONS
# ============================

# Обо мне → ссылка
@router.message(F.text == "Обо мне")
async def about_me(message: Message):
    await message.answer(
        "Обо мне:\nhttps://telegra.ph/Obo-mne-07-07-18"
    )


# Записаться на консультацию → текст + ссылка в слове «анкета»
@router.message(F.text == "Записаться на консультацию")
async def sign_up(message: Message):
    await message.answer(
        "К сожалению, на данный момент окна для записи в личную терапию с Елизаветой отсутствуют.\n\n"
        "Для записи в лист ожидания заполните [анкету](https://forms.gle/TmUVpdhyY7ASCnqDA).",
        parse_mode="Markdown"
    )


# 12 взрослых колыбельных → ссылка
@router.message(F.text == "12 взрослых колыбельных")
async def lullabies(message: Message):
    await message.answer(
        "12 взрослых колыбельных:\nhttps://t.me/your_mental_doc/131"
    )


# Синемалогия → переход на старт синемалогии
@router.message(F.text == "Синемалогия")
async def cinemalogy_start(message: Message):
    from handlers.cinemalogy.start import start_cinemalogy
    await start_cinemalogy(message)
