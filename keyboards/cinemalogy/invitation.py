"""
Клавиатура приглашения на кинопоказ.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def invitation_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎟 Мини",
                    callback_data="tariff_mini"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Миди",
                    callback_data="tariff_midi"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Макси",
                    callback_data="tariff_maxi"
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
