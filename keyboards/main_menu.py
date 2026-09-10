from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Обо мне")
        ],
        [
            KeyboardButton(text="Записаться на консультацию")
        ],
        [
            KeyboardButton(text="12 взрослых колыбельных")
        ],
        [
            KeyboardButton(text="Синемалогия")
        ],
        [
            KeyboardButton(text="⚖️ Правовая информация")
        ]
    ],
    resize_keyboard=True
)

