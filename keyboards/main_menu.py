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
        ]
    ],
    resize_keyboard=True
)

