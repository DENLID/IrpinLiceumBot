from aiogram import F, Router
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.error_event import ErrorEvent

router = Router()

@router.errors(ExceptionTypeFilter(TelegramBadRequest))
async def error_handler(event: ErrorEvent):
    if event.exception == "Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message":
        pass