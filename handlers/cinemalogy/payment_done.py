"""
Шаг 10. Экран после подтверждения оплаты
Пользователь нажал кнопку «Билет оплачен»
"""

from aiogram import Router
from aiogram.types import CallbackQuery

# Главное меню
from keyboards.main_menu import main_menu
from bot_services.user_parameters import get_parameter
from bot_services.admin_notifications import notify_admin_payment_done

router = Router()


@router.callback_query(lambda c: c.data == "payment_done")
async def payment_done(callback: CallbackQuery):
    """
    Шаг 10
    Пользователь подтвердил оплату
    Показываем благодарность, ссылку на канал и возвращаем главное меню
    """

    # удаляем экран оплаты
    try:
        await callback.message.delete()
    except Exception:
        pass

    telegram_id = callback.from_user.id
    tariff = get_parameter(telegram_id, "cinemalogy_tariff")

    # сообщение пользователю
    await callback.message.answer(
        (
            "Благодарю!\n\n"
            "Бот пришлет ваш билет в течение суток после оплаты 🤗\n"
            "В случае возникновения вопросов по оплате пишите напрямую мне @saeliz\n\n"
            "Если вы хотите приобрести еще билеты, нажмите кнопку «Синемалогия» ниже\n\n"
            "Для более тесного знакомства приглашаю вас в мой телеграм‑"
            "<a href=\"https://t.me/your_mental_doc\">канал</a>\n\n"
            "Тут мои заметки на темы отношений: с собой, миром и партнером. "
            "Анонсы мероприятий и открытых окон в работу со мной"
        ),
        reply_markup=main_menu,
        parse_mode="HTML"
    )

    await callback.answer()

    # уведомление админу — теперь с указанием тарифа
    await notify_admin_payment_done(callback.bot, callback.from_user, tariff)
