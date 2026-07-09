"""
Клавиатура оплаты.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def payment_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Билет оплачен",
                    callback_data="payment_done"
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
