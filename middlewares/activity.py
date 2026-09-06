from aiogram import BaseMiddleware

from bot_services.database import (
    get_user,
    update_last_activity
)

from bot_services.database import add_event

class ActivityMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler,
        event,
        data
    ):

        user = event.from_user

        if user:

            existing_user = get_user(user.id)

            if existing_user:

                update_last_activity(user.id)

                # getattr, не hasattr: у Message поле "text" есть всегда
                # (None для медиа), а у CallbackQuery его нет вовсе —
                # hasattr(event, "text") было истинно для любого Message,
                # включая фото/стикеры, и писало "message" с event_data=None.
                text = getattr(event, "text", None)

                if text:
                    add_event(
                        user.id,
                        "message",
                        text
                    )

        return await handler(
            event,
            data
        )
