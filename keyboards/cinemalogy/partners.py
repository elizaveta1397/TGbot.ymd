from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def partners_carousel_keyboard(index: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data=f"partners_prev:{index}"),
            InlineKeyboardButton(text="➡️", callback_data=f"partners_next:{index}")
        ],
        [
            InlineKeyboardButton(text="Приглашение на показ", callback_data="invitation")
        ]
    ])
