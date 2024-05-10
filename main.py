import asyncio, logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from motor.motor_asyncio import AsyncIOMotorClient
from threading import Thread

from errors import errors
from handlers import user_commands, air_alert, communication, webappdata, ms, confirm_person
from callbacks import callbacks
from air_alert.air_alert import pull_air_alert
from middlewares.anti_flood import AntiFloodMiddleware
import config

async def main():
    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    cluster = AsyncIOMotorClient(config.mongo_api)
    db = cluster.ILdb

    dp.message.middleware(AntiFloodMiddleware())

    dp.include_routers(
        user_commands.router,
        air_alert.router,
        webappdata.router,
        communication.router,
        confirm_person.router,
        ms.router,
        callbacks.router,
        errors.router
    )

    th = Thread(target=pull_air_alert).start()

    #logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())

