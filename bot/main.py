import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import admin, stats
from bot.config import settings
from bot.db import create_pool
from bot.handlers import admin, registration, requests, start, stats, metrics 
from bot.services.manager_service import sync_default_staff
from bot.handlers import applications as applications_handler


async def main():
    logging.basicConfig(level=logging.INFO)
    await create_pool()

    bot = Bot(token=settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(registration.router)
    dp.include_router(requests.router)
    dp.include_router(stats.router)
    dp.include_router(applications_handler.router)
    dp.include_router(metrics.router)
    
  

    await sync_default_staff(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())