from aiogram.types import Message
from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from motor.core import AgnosticDatabase as MDB

from utils.states import MS_state
from filters.filters import IsAdminChat, IsWadMessage
import keyboards.keyboards as keyboards
import config


router = Router()

async def success_message(message: Message):
    await message.answer("Пункт успішно змінено ✅", reply_markup=keyboards.back_ms)

@router.message(MS_state.students_number)
async def handle_students_number(message: Message, state: FSMContext):
    await state.update_data(students_number=message.text)
    await success_message(message)

@router.message(MS_state.ms_number)
async def handle_ms_number(message: Message, state: FSMContext):
    await state.update_data(ms_number=message.text)
    await success_message(message)

@router.message(MS_state.ms_number_hv)
async def handle_ms_number_hv(message: Message, state: FSMContext):
    await state.update_data(ms_number_hv=message.text)
    await success_message(message)

@router.message(MS_state.ms)
async def handle_ms(message: Message, state: FSMContext):
    await state.update_data(ms=message.text)
    await success_message(message)
