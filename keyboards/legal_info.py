from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import PRIVACY_POLICY_URL


def legal_info_keyboard() -> InlineKeyboardMarkup:
    """
    Раздел «Правовая информация» из главного меню — собирает в одном
    месте документы/действия, которые раньше были разбросаны по
    отдельным командам (152-ФЗ) — см. docs/IDEAS.md, п.12.
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
                    text="💬 Связаться с оператором ПДн",
                    url="https://t.me/goncharova_help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Удалить мои данные",
                    callback_data="legal_delete_me"
                )
            ]
        ]
    )
