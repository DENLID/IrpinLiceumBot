from aiogram.types import Message
from aiogram import Router, Bot, F
from pytz import timezone
from datetime import datetime
from motor.core import AgnosticDatabase as MDB

import config


router = Router()


@router.channel_post()
async def airalert_handler(message: Message, db: MDB, bot: Bot):
    if message.chat.id == config.channel_all_to:
        ukraine_time = timezone('Europe/Kiev')
        dt = datetime.now(ukraine_time)
        weekday = dt.weekday()
        
        if weekday != 5 and weekday != 6 and datetime(dt.year, dt.month, dt.day, 8, 0, tzinfo=ukraine_time) <= dt <= datetime(dt.year, dt.month, dt.day, 17, 30, tzinfo=ukraine_time):
            async for u in db.users.find({"airalert": "st"}):
                try:
                    await message.copy_to(u["_id"]) # Надсилання користувачам
                except:
                    pass
            await message.copy_to(config.channel_to) # Надсилання на канал
            
        
        async for u in db.users.find({"airalert": "always"}):
            try:
                await bot.send_message(u["_id"], "<b>Увага! Повітряна тривога</b> 🔴")
            except:
                pass
