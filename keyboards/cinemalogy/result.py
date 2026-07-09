"""
Клавиатура результата выбора кадра.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def result_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟 Приглашение на показ",
                    callback_data="cinemalogy_invitation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="cinemalogy_home"
                )
            ]
        ]
    )
