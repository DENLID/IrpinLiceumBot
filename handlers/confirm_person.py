from aiogram.types import Message
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from utils.states import ConfirmPerson
from utils.utils import send_email
from filters.filters import IsAdminChat
import keyboards.keyboards as keyboards
import config


router = Router()


@router.message(ConfirmPerson())
async def handle_email(message: Message, bot: Bot):
    text = message.text
    send_email(receiver=text, text="HELOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    