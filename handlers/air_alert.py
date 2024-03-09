from aiogram.types import Message
from aiogram import Router, Bot, F
from pytz import timezone
from datetime import datetime

from pymongo import MongoClient

import keyboerds.keyboards as keyboards
import config


router = Router()

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


@router.channel_post()
async def airalert_handler(message: Message):
    if message.chat.id == config.channel_all_to:
        ukraine_time = timezone('Europe/Kiev')
        dt = datetime.now(ukraine_time)
        weekday = dt.weekday()
        
        if weekday != 5 and weekday != 6 and datetime(dt.year, dt.month, dt.day, 8, 0, tzinfo=ukraine_time) <= dt <= datetime(dt.year, dt.month, dt.day, 18, 40, tzinfo=ukraine_time):
            for u in users.find({ "$or": [{"airalert": "st"}, {"airalert": "always"}]}):
                await message.copy_to(u["_id"]) # Надсилання користувачам
            await message.copy_to(config.channel_to) # Надсилання на канал
        else:
            for u in users.find({"airalert": "always"}):
                await message.copy_to(u["_id"])