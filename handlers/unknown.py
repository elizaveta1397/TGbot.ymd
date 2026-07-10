from aiogram import Router
from aiogram.types import Message

router = Router()

async def process_unknown(message: Message):
    await message.answer("Команда не распознана. Попробуйте ещё раз.")
