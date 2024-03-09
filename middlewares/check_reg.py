from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users

class CheckRegistration(BaseMiddleware):
    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        print("gg")
        id = int(event.chat.id)
        
        y = {
            "_id": id,
            "username": event.from_user.username,
            "airalert": "never",
            "tags": []
        }

        is_exist = users.count_documents({"_id": id})
        
        if is_exist == 0:
            users.insert_one(y)
        return await handler(event, data)