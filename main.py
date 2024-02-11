import asyncio, logging
from aiogram import Bot, Dispatcher
from threading import Thread

import handlers
import callbacks
from air_alert import air_alert
import config

async def main():
    bot = Bot(config.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(
        handlers.router,
        callbacks.router
    )

    th = Thread(target=air_alert).start()

    #logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

