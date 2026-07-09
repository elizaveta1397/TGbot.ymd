"""
Клавиатура экрана тарифа.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def tariff_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Приобрести билет",
                    callback_data="payment"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Другие варианты",
                    callback_data="cinemalogy_invitation"
                )
            ]
        ]
    )
