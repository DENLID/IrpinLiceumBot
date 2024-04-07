from typing import List
from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message
from motor.core import AgnosticDatabase as MDB
import config


class IsAdminChat(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.id == config.admin_group
    
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, db: MDB) -> bool:
        user = await db.users.find_one({"_id": message.chat.id})
        return "admin" in user["tags"]

class IsMsAdmin(BaseFilter):
    async def __call__(self, message: Message, db: MDB) -> bool:
        user = await db.users.find_one({"_id": message.chat.id})
        return "ms_admin" in user["tags"]

class IsWadMessage(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.web_app_data != None
    
class CheckArg(BaseFilter):
    def __init__(self, value) -> None:
        self.value = value

    async def __call__(self, message: Message, command: CommandObject) -> bool:
        arg = command.args
        return arg == self.value