from aiogram import BaseMiddleware

from bot_services.database import get_user

# Команды и callback_data, которые обязаны работать ДО регистрации/
# согласия — иначе пользователю, который ещё не согласился, будет
# не из чего выбирать (не увидит ни политику, ни саму кнопку
# согласия).
ALLOWED_COMMANDS = {"/start", "/policy"}
ALLOWED_CALLBACK_DATA = {"consent_accept", "policy_view"}

NOT_CONSENTED_TEXT = (
    "Чтобы пользоваться ботом, сначала нужно принять условия "
    "обработки персональных данных — напишите /start."
)


class ConsentGateMiddleware(BaseMiddleware):
    """
    Блокирует любое действие в боте (кнопки меню, шаги воронок,
    произвольные сообщения) для пользователя, у которого нет строки
    в users — то есть который ещё не нажал «Согласен(на)» на экране
    согласия (handlers/start.py::consent_accept).

    Без этой проверки пользователь мог пройти по сценариям бота, не
    принимая условия вовсе — например, нажав старую кнопку главного
    меню или инлайн-кнопку, оставшуюся на экране с прошлой сессии в
    Telegram-клиенте, в обход самого экрана согласия. См.
    docs/IDEAS.md, п.1.
    """

    async def __call__(
        self,
        handler,
        event,
        data
    ):

        user = event.from_user

        if user is None:
            return await handler(event, data)

        text = getattr(event, "text", None)
        if text:
            command = text.split()[0].split("@")[0]
            if command in ALLOWED_COMMANDS:
                return await handler(event, data)

        callback_data = getattr(event, "data", None)
        if callback_data in ALLOWED_CALLBACK_DATA:
            return await handler(event, data)

        if get_user(user.id) is not None:
            return await handler(event, data)

        await event.answer(NOT_CONSENTED_TEXT)
        return None
