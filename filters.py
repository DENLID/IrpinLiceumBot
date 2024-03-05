from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message
from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


class IsAdminChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id == config.admin_group
    
class IsMsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return "ms_admin" in users.find_one({"_id": message.chat.id})["tags"]

class IsWadMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.web_app_data != None