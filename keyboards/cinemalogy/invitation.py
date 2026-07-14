"""
Клавиатура приглашения на кинопоказ.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def invitation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟 Билет Mini",
                    callback_data="tariff_mini"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Билет Midi",
                    callback_data="tariff_midi"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Билет Maxi",
                    callback_data="tariff_maxi"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🫂 Партнеры показа",
                    callback_data="cinemalogy_partners"
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
