"""
Модуль: Партнёры кинопоказа.
Отображает изображения партнёров в виде бесконечной карусели.
Работает с таблицей materials_cinemalogy через сервис get_material().
"""

from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto
)

# ВАЖНО: используем правильный сервис Cinemalogy
from bot_services.cinemalogy.materials import get_material

router = Router()


def partners(index: int):
    """
    Клавиатура карусели партнёров.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"partners_prev:{index}"
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"partners_next:{index}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Приглашение на показ",
                    callback_data="cinemalogy_invitation"   # ← исправлено
                )
            ]
        ]
    )


def get_partners_images():
    """
    Получение всех изображений партнёров.
    Перебираем ключи cinemalogy_partners_image_01, 02, 03...
    """
    images = []
    index = 1

    while True:
        key = f"cinemalogy_partners_image_{index:02d}"
        material = get_material(key)

        if not material:
            break

        images.append(material)
        index += 1

    return images


@router.callback_query(lambda c: c.data == "partners")
async def partners_start(callback: CallbackQuery):
    """
    Первый экран карусели партнёров.
    """

    # Удаляем предыдущее сообщение
    try:
        await callback.message.delete()
    except Exception:
        pass

    images = get_partners_images()
    index = 0

    await callback.message.answer_photo(
        images[index]["telegram_file_id"],
        reply_markup=partners(index)
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("partners_next"))
async def partners_next(callback: CallbackQuery):
    """
    Листание вперёд.
    """
    images = get_partners_images()
    count = len(images)

    current_index = int(callback.data.split(":")[1])
    new_index = (current_index + 1) % count

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=images[new_index]["telegram_file_id"]
        ),
        reply_markup=partners(new_index)
    )

    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("partners_prev"))
async def partners_prev(callback: CallbackQuery):
    """
    Листание назад.
    """
    images = get_partners_images()
    count = len(images)

    current_index = int(callback.data.split(":")[1])
    new_index = (current_index - 1) % count

    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=images[new_index]["telegram_file_id"]
        ),
        reply_markup=partners(new_index)
    )

    await callback.answer()
