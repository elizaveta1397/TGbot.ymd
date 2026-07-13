from bot_services.cinemalogy.materials import get_material

async def back_to_frames(callback, telegram_id):
    current_frame = get_parameter(
        telegram_id,
        "cinemalogy_current_frame"
    )

    image = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_image"
    )

    text = get_material(
        f"cinemalogy_frame_{int(current_frame):02d}_text"
    )

    await callback.message.answer_photo(
        photo=image["telegram_file_id"],
        caption=text["text"] if text else "",
        reply_markup=frame_keyboard()
    )
