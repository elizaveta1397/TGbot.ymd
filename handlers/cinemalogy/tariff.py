"""
Шаг 7. Экран выбранного тарифа.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.tariffs import tariff_keyboard

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter
from bot_services.cinemalogy.materials import get_material

router = Router()


async def send_tariff(callback: CallbackQuery, tariff_code: str):

    telegram_id = callback.from_user.id

    # удаляем предыдущий экран
    try:
        await callback.message.delete()
    except:
        pass

    # записываем шаг
    set_parameter(telegram_id, "current_step", f"tariff_{tariff_code}")

    # аналитика
    add_event(telegram_id, "cinemalogy_tariff_selected", tariff_code)

    # материалы
    image_row = get_material(f"ticket_{tariff_code}_image")
    text_row = get_material(f"ticket_{tariff_code}_text")

    await callback.message.answer_photo(
        photo=image_row["telegram_file_id"],
        caption=text_row["text"],
        reply_markup=tariff_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "tariff_mini")
async def tariff_mini(callback: CallbackQuery):

    telegram_id = callback.from_user.id
    set_parameter(telegram_id, "cinemalogy_tariff", "mini")   # ← ДОБАВЛЕНО

    await send_tariff(callback, "mini")


@router.callback_query(F.data == "tariff_midi")
async def tariff_midi(callback: CallbackQuery):

    telegram_id = callback.from_user.id
    set_parameter(telegram_id, "cinemalogy_tariff", "midi")   # ← ДОБАВЛЕНО

    await send_tariff(callback, "midi")


@router.callback_query(F.data == "tariff_maxi")
async def tariff_maxi(callback: CallbackQuery):

    telegram_id = callback.from_user.id
    set_parameter(telegram_id, "cinemalogy_tariff", "maxi")   # ← ДОБАВЛЕНО

    await send_tariff(callback, "maxi")
