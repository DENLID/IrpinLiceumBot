import asyncio, logging
from aiogram import Bot, Dispatcher
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB
from threading import Thread

from handlers import user_commands, air_alert
from callbacks import callbacks
from air_alert.air_alert import pull_air_alert
from middlewares.anti_flood import CheckRegistration
import config

async def main():
    bot = Bot(config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    cluster = AsyncIOMotorClient(config.mongo_api)
    db = cluster.ILdb

    #dp.message.middleware(CheckRegistration())

    dp.include_routers(
        user_commands.router,
        air_alert.router,
        callbacks.router
    )

    th = Thread(target=pull_air_alert).start()

    #logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())

