# bot.py

from handlers.cinemalogy import router as cinemalogy_router
from handlers.admin import router_admin_callbacks, router_admin_messages
from handlers.unknown import router as unknown_router
from handlers.consultation import router as consultation_router

from bot_services.database import (
    create_tables,
    cleanup_old_events
)

import asyncio

from aiogram import Bot, Dispatcher

from handlers.start import router as start_router

from config import BOT_TOKEN

from middlewares.activity import ActivityMiddleware
from middlewares.consent_gate import ConsentGateMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ConsentGate — раньше ActivityMiddleware: блокировать несогласившихся
# нужно до того, как что-либо ещё их сообщение обработает.
dp.message.middleware(
    ConsentGateMiddleware()
)
dp.callback_query.middleware(
    ConsentGateMiddleware()
)

dp.message.middleware(
    ActivityMiddleware()
)
dp.callback_query.middleware(
    ActivityMiddleware()
)

dp.include_router(start_router)
dp.include_router(cinemalogy_router)
dp.include_router(router_admin_callbacks)
dp.include_router(router_admin_messages)
dp.include_router(consultation_router)

dp.include_router(unknown_router)

async def main():
    create_tables()
    cleanup_old_events()

    print("Бот запускается")
    print("Начинаем polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
