# keyboards/consultation_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def consultation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Записаться в лист ожидания",
                    url="https://t.me/goncharova_help"
                )
            ]
        ]
    )
