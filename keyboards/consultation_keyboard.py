# keyboards/consultation_keyboard.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def consultation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Записаться в лист ожидания",
                    url="https://docs.google.com/forms/d/e/1FAIpQLSeTHGnQV6W4QOO7Q4pBhG722J1nj3oN5RorFTLJXnHKoGycYg/viewform?usp=send_form"
                )
            ]
        ]
    )
