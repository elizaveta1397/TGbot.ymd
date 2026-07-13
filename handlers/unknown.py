from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def process_unknown(message: Message):
    await message.answer(
        "Я не понял сообщение. Используйте кнопки меню или нажмите /start."
    )
