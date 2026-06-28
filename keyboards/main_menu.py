from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

# ===== Главное меню =====

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📖 Обо мне")
        ],
        [
            KeyboardButton(text="📝 Записаться")
        ],
        [
            KeyboardButton(text="🎁 Бесплатный материал")
        ],
        [
            KeyboardButton(text="❓ Задать вопрос")
        ]
    ],
    resize_keyboard=True
)
