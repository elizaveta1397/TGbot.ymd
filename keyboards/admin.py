from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔁 Переключить режим",
                    callback_data="admin_toggle"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Дать доступ",
                    callback_data="admin_grant"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➖ Забрать доступ",
                    callback_data="admin_revoke"
                )
            ]
        ]
    )
