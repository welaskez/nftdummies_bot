from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from nftdummies_bot.handlers import routers
from nftdummies_bot.db.engine import session_maker, create_db
from nftdummies_bot.middlewares import DatabaseSession
from nftdummies_bot import config

import asyncio

import logging


bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
    ),
)
dp = Dispatcher()


async def on_startup(bot: Bot):
    await create_db()
    logging.info("Bot has started")


async def on_shutdown(bot: Bot):
    logging.info("Bot has finished the job!")


async def main():
    dp.include_routers(*routers)
    dp.update.middleware(DatabaseSession(session_pool=session_maker))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("bot.log")],
    )
    asyncio.run(main())
