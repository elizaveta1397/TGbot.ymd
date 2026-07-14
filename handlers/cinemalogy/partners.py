from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "cinemalogy_partners")
async def partners(callback: CallbackQuery):

    await callback.message.answer(
        "Экран партнёров показа будет добавлен позже."
    )

    await callback.answer()
