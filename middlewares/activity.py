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

                if hasattr(event, "text"):
                    add_event(
                        user.id,
                        "message",
                        event.text
                    )

        return await handler(
            event,
            data
        )
