from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.error_event import ErrorEvent

router = Router()

@router.errors(ExceptionTypeFilter(TelegramBadRequest))
def error_handler(event: ErrorEvent):
    print(f"DAAAA: {event.exception}")