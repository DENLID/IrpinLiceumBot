from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
import config


class CheckRegistration(BaseMiddleware):
    def __init__(self, db) -> None:
        self.db = db

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:     
        
        return await handler(event, data)