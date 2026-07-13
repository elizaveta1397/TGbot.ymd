from aiogram import Router
from aiogram.types import Message
from bot_services.database import add_event

router = Router()


# ===== Обо мне =====

@router.message(lambda message: message.text == "📖 Обо мне")
async def about_handler(message: Message):

    add_event(
        message.from_user.id,
        "button_click",
        "about"
    )

    await message.answer(
        "Здесь будет информация о психологе."
    )
