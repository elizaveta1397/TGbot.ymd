from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Подтверждение перед необратимым удалением данных пользователя
    (152-ФЗ, ст. 14) — см. docs/IDEAS.md, п.1.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Да, удалить всё",
                    callback_data="delete_me_confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="delete_me_cancel"
                )
            ]
        ]
    )
