from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import or_f
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.error_event import ErrorEvent
from colorama import Fore, Style

router = Router()


@router.errors(ExceptionTypeFilter(TelegramBadRequest))
async def error_handler(event: ErrorEvent):
    if str(event.exception) == "Telegram server says - Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message":
        pass
    else:
        print(f"{event.exception}")


@router.errors(
    or_f(ExceptionTypeFilter(AttributeError), ExceptionTypeFilter(ValueError)),
    F.update.message.as_("message"),
)
async def error_handler(event: ErrorEvent, message: Message):
    if str(
        event.exception
    ) == "'NoneType' object has no attribute 'split'" or "invalid literal for int() with base 10" in str(
        event.exception
    ):
        await message.answer("Не коректний запис команди ❌")
    else:
        print(f"'{event.exception}'")


@router.errors(ExceptionTypeFilter(TypeError))
async def error_handler(event: ErrorEvent):
    if str(event.exception) == "'_asyncio.Future' object is not subscriptable":
        print(f"{event.exception}")
        print(Fore.RED + "Походу ти десь забув await!" + Style.RESET_ALL)
    else:
        print(f"{event.exception}")
