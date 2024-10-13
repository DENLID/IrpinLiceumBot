from aiogram.types import Message
from aiogram import Router, Bot, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from motor.core import AgnosticDatabase as MDB
from random import randint

from utils.states import ConfirmPerson
from utils.utils import send_email
from filters.filters import IsAdminChat
import keyboards.keyboards as keyboards
import config


router = Router()

verify_codes = {}


async def send_email_code(message: Message, email: str, state: FSMContext):
    code = f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"

    verify_codes[message.chat.id] = code

    send_email(receiver=email, text=f"""
Привіт!

Твій верифікаційний код: {code}

Якщо ви не очікували цього повідомлення, просто проігноруйте його.
""")
    await message.answer("Код успішно надіслано ✅", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Надіслати ще раз",
            callback_data="send_email_code"
        )
    ]]))
    await state.set_state(ConfirmPerson.email_code)


@router.message(ConfirmPerson.email)
async def handle_email(message: Message, state: FSMContext):
    await send_email_code(message, message.text, state)
    

@router.message(ConfirmPerson.email_code)
async def handle_email_code(message: Message, bot: Bot, db: MDB):
    text = message.text

    if verify_codes[message.chat.id] == text:
        await db.users.update_one({"_id": message.chat.id}, {"$pull": {"tags": "verified"}})
