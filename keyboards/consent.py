from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import PRIVACY_POLICY_URL


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
                    url=PRIVACY_POLICY_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Даю согласие на обработку персональных данных",
                    callback_data="consent_accept"
                )
            ]
        ]
    )
