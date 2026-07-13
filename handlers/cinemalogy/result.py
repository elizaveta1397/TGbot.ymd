"""
Шаг 5. Результат выбора кадра.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot_services.database import add_event
from bot_services.user_parameters import (
    get_parameter,
    set_parameter,
    delete_parameter
)

from keyboards.cinemalogy.result import result_keyboard

router = Router()


@router.callback_query(F.data == "confirm_frame")
async def result(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    # Удаляем сообщение с гифкой подтверждения
    try:
        await callback.message.delete()
    except Exception:
        pass

    frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    admin_mode = get_parameter(
        telegram_id,
        "admin_mode"
    )

    # Если включен режим администратора,
    # удаляем старый выбор
    if admin_mode == "on":
        delete_parameter(
            telegram_id,
            "cinemalogy_choice"
        )

    # Записываем окончательный выбор пользователя
    set_parameter(
        telegram_id,
        "cinemalogy_choice",
        frame
    )

    # Текущий шаг
    set_parameter(
        telegram_id,
        "current_step",
        "result"
    )

    # Аналитика
    add_event(
        telegram_id,
        "cinemalogy_result",
        frame
    )

    # Получаем изображение выбранного кадра
    from bot_services.cinemalogy.materials import get_material

    image_row = get_material(
        f"cinemalogy_frame_{int(frame):02d}_image"
    )

    # Текст результата — если есть отдельный текст
    text_row = get_material(
        f"cinemalogy_frame_{int(frame):02d}_result_text"
    )

    result_text = text_row["text"] if text_row else "Ваш выбор сохранён."

    # Получаем текст кнопки статьи
    article_button_row = get_material(
        f"cinemalogy_frame_{int(frame):02d}_article_button"
    )

    # Получаем URL статьи
    article_url_row = get_material(
        f"cinemalogy_frame_{int(frame):02d}_article_url"
    )

    article_button_text = article_button_row["text"]
    article_url = article_url_row["url"]

    # Отправляем результат
    await callback.message.answer_photo(
        photo=image_row["telegram_file_id"],
        caption=result_text,
        reply_markup=result_keyboard(
            article_button_text,
            article_url
        )
    )

    await callback.answer()
