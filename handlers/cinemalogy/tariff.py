"""
Шаг 7.
Экран выбранного тарифа.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.cinemalogy.tariffs import tariff_keyboard

from bot_services.database import add_event
from bot_services.user_parameters import set_parameter

router = Router()


@router.callback_query(
    F.data.in_(
        [
            "tariff_mini",
            "tariff_midi",
            "tariff_maxi"
        ]
    )
)
async def tariff(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    tariff = callback.data.replace(
        "tariff_",
        ""
    )

    # Запоминаем выбранный тариф
    set_parameter(
        telegram_id,
        "cinemalogy_tariff",
        tariff
    )

    # Запоминаем текущий шаг
    set_parameter(
        telegram_id,
        "current_step",
        "tariff"
    )

    # Аналитика
    add_event(
        telegram_id,
        "cinemalogy_tariff_selected",
        tariff
    )

    # --- ХАРДКОД ТЕКСТОВ ТАРИФОВ ---
    texts = {
        "mini": "Описание тарифа мини.",
        "midi": "Описание тарифа мини.",   # ты прислала два одинаковых текста
        "maxi": "Описание тарифа максимум."
    }

    # --- ХАРДКОД КАРТИНОК (оставляем как есть, таблица не трогается) ---
    from bot_services.cinemalogy.materials import get_material
    image_row = get_material(f"ticket_{tariff}_image")
    # --------------------------------------

    await callback.message.answer_photo(
        photo=image_row["telegram_file_id"],
        caption=texts[tariff],
        reply_markup=tariff_keyboard()
    )

    await callback.answer()
