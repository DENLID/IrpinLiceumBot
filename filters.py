from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message
from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


class IsAdmin(BaseFilter):
    def __init__(self, is_not: bool=False) -> None:
        self.is_not = is_not
    async def __call__(self, message: Message) -> bool:
        if self.is_not == False:
            return message.chat.id in config.admins
        else:
            return message.chat.id not in config.admins