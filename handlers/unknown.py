from aiogram import Router, F
from aiogram.types import Message

router = Router()

ADMIN_ID = 250428280
ADMIN_WORDS = ("адм", "админ", "admin", "adm")


def is_admin_command(text: str) -> bool:
    if not text:
        return False
    tl = text.strip().lower()
    return any(tl.startswith(w) for w in ADMIN_WORDS)


@router.message(F.text)
async def process_unknown(message: Message):

    # --- Админ-команда ---
    if is_admin_command(message.text):
        if message.from_user.id == ADMIN_ID:
            from handlers.admin import show_admin_menu
            await show_admin_menu(message)
            return
        else:
            await message.answer("Вы не админ.")
            return

    # --- Обычный unknown ---
    await message.answer(
        "Я не понял сообщение. Используйте кнопки меню или нажмите /start."
    )
