"""
Клавиатура выбора кадра.
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton


def frame_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data="frame_prev"
                ),
                InlineKeyboardButton(
                    text="Выбрать",
                    callback_data="frame_select"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data="frame_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="cinemalogy_home"
                )
            ]
        ]
    )


def confirm_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтверждаю",
                    callback_data="confirm_frame"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Посмотреть другие",
                    callback_data="back_to_frames"
                )
            ]
        ]
    )
