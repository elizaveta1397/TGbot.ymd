"""
Шаг 4. Подтверждение выбора кадра.
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

from services.database import add_event
from services.user_parameters import (
    get_parameter,
    set_parameter
)

from keyboards.cinemalogy.frames import confirm_keyboard

router = Router()


@router.callback_query(F.data == "frame_select")
async def frame_select(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    current_frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    set_parameter(
        telegram_id,
        "current_step",
        "confirm_frame"
    )

    add_event(
        telegram_id,
        "confirm_frame",
        current_frame
    )

    from services.cinemalogy.materials import get_material

    # Удаляем сообщение с кадром
    try:
        await callback.message.delete()
    except Exception:
        pass

    # Гифка подтверждения
    gif = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_confirm_gif"
    )

    # Название фильма
    movie_title_row = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_movie_title"
    )
    movie_title = movie_title_row["text"] if movie_title_row else ""

    # Новый текст
    caption_text = (
        f"{movie_title}\n\n"
        "Кадр из фильма можно выбрать только один раз\n\n"
        "Для подтверждения выбора нажмите на кнопку ниже"
    )

    await callback.message.answer_animation(
        animation=gif["telegram_file_id"] if gif and gif["telegram_file_id"] else None,
        caption=caption_text,
        reply_markup=confirm_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_frames")
async def back_to_frames(callback: CallbackQuery):

    telegram_id = callback.from_user.id

    # Удаляем сообщение с гифкой подтверждения
    try:
        await callback.message.delete()
    except Exception:
        pass

    # Берём кадр, который был до подтверждения
    current_frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    from services.cinemalogy.materials import get_material
    from keyboards.cinemalogy.frames import frame_keyboard

    # Получаем изображение кадра
    image = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_image"
    )

    # Показываем тот же кадр
    await callback.message.answer_photo(
        photo=image["telegram_file_id"],
        caption=(
            "Внимательно посмотрите на кадры из фильмов. Не оценивайте их критически\n\n"
            "Выберите тот, который первым вызвал наиболее сильный эмоциональный отклик"
        ),
        reply_markup=frame_keyboard()
    )

    await callback.answer()
