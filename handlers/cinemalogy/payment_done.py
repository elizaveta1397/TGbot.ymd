from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "payment_done")
async def payment_done(callback: CallbackQuery):
    # Сообщение пользователю
    await callback.message.answer(
        "Спасибо! Ваш билет успешно оплачен. Мы скоро с вами свяжемся."
    )
    await callback.answer()

    # Сообщение админу
    admin_id = 250428280  # твой Telegram ID
    await callback.bot.send_message(
        admin_id,
        f"Пользователь @{callback.from_user.username} (ID: {callback.from_user.id}) оплатил билет."
    )
