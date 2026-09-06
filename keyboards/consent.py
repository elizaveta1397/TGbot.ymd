from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def consent_keyboard() -> InlineKeyboardMarkup:
    """
    Экран согласия на обработку персональных данных перед регистрацией
    нового пользователя (152-ФЗ) — см. docs/IDEAS.md, п.1.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Читать политику",
                    callback_data="policy_view"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Согласен(на) на обработку персональных данных",
                    callback_data="consent_accept"
                )
            ]
        ]
    )
