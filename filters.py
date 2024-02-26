from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message
from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id in config.admins