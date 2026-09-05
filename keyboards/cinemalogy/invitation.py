"""
Клавиатура приглашения на кинопоказ.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def invitation_keyboard(show_partners: bool = True):

    rows = [
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
    ]

    # Кнопку прячем, если в materials_cinemalogy нет ни одного
    # активного партнёра — иначе partners_start() упадёт на пустом
    # списке (см. handlers/cinemalogy/partners.py)
    if show_partners:
        rows.append(
            [
                InlineKeyboardButton(
                    text="🫂 Партнеры показа",
                    callback_data="partners"
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="cinemalogy_home"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)
