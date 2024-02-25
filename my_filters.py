from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message

import config

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if isinstance(config.admins, int):
            return config.admins == message.chat.id