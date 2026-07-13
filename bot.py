from bot_services.database import create_tables
from handlers.cinemalogy import router as cinemalogy_router
from handlers.admin import router_admin_callbacks
from handlers.unknown import router as unknown_router

from bot_services.database import (
    create_tables,
    cleanup_old_events
)

import asyncio

from aiogram import Bot, Dispatcher

from handlers.start import router as start_router

from config import BOT_TOKEN

from middlewares.activity import ActivityMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.message.middleware(
    ActivityMiddleware()
)

dp.include_router(start_router)
dp.include_router(cinemalogy_router)
dp.include_router(router_admin_callbacks)

dp.include_router(unknown_router)

async def main():
    create_tables()
    cleanup_old_events()

    print("Бот запускается")
    print("Начинаем polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
