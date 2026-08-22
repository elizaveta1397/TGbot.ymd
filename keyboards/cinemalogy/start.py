from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_keyboard():

    # Жёстко прописываем URL — без таблиц
    about_author_url = "https://telegra.ph/Obo-mne-07-14-13"
    about_cinemalogy_url = "https://telegra.ph/O-sinemalogii-07-07-2"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Выбрать кадр",
                    callback_data="cinemalogy_choose_frame"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎟 Приглашение на показ",
                    callback_data="cinemalogy_invitation"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Обо мне",
                    url=about_author_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎥 О синемалогии",
                    url=about_cinemalogy_url
                )
            ]
        ]
    )


def start_keyboard_v2():

    about_author_url = "https://telegra.ph/Obo-mne-07-14-13"
    about_cinemalogy_url = "https://telegra.ph/O-sinemalogii-07-07-2"
    lullabies_url = "https://t.me/your_mental_doc/131"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 О синемалогии",
                    url=about_cinemalogy_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Обо мне",
                    url=about_author_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Записаться на консультацию",
                    callback_data="consultation_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎶 12 взрослых колыбельных",
                    url=lullabies_url
                )
            ]
        ]
    )
