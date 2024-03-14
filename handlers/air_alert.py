from aiogram.types import Message
from aiogram import Router, Bot, F
from pytz import timezone
from datetime import datetime
from motor.core import AgnosticDatabase as MDB

import keyboards.keyboards as keyboards
import config


router = Router()


@router.channel_post()
async def airalert_handler(message: Message, db: MDB):
    if message.chat.id == config.channel_all_to:
        ukraine_time = timezone('Europe/Kiev')
        dt = datetime.now(ukraine_time)
        weekday = dt.weekday()
        
        if weekday != 5 and weekday != 6 and datetime(dt.year, dt.month, dt.day, 8, 0, tzinfo=ukraine_time) <= dt <= datetime(dt.year, dt.month, dt.day, 18, 40, tzinfo=ukraine_time):
            for u in await db.users.find({ "$or": [{"airalert": "st"}, {"airalert": "always"}]}):
                print("send air alert to channel")
                await message.copy_to(u["_id"]) # Надсилання користувачам
            await message.copy_to(config.channel_to) # Надсилання на канал
        else:
            for u in await db.users.find({"airalert": "always"}):
                await message.copy_to(u["_id"])
