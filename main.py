import asyncio, logging
from aiogram import Bot, Dispatcher
from threading import Thread

from handlers import user_commands, air_alert
from callbacks import callbacks
from air_alert import air_alert
from middlewares.check_reg import CheckRegistration
import config

async def main():
    bot = Bot(config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    dp.message.middleware(CheckRegistration())

    dp.include_routers(
        user_commands.router,
        air_alert.router,
        callbacks.router
    )

    th = Thread(target=air_alert).start()

    #logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

