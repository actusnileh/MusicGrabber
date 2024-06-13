import asyncio
import logging
from aiogram import Bot, Dispatcher

from common.settings import settings

from handlers.start import router as start_router
from handlers.music import router as music_router
from handlers.search import router as search_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=settings.token)
    dp = Dispatcher()

    dp.include_routers(start_router, music_router, search_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
