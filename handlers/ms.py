from aiogram.types import Message
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from utils.states import MS_state
from filters.filters import IsAdminChat, IsWadMessage, IsMsAdmin
import keyboards.keyboards as keyboards
import config


router = Router()

 
@router.message(MS_state.students_number)
async def handle_text(message: Message):

@router.message(MS_state.ms_number)
async def handle_text(message: Message):

@router.message(MS_state.ms_number_hv)
async def handle_text(message: Message, bot: Bot):

@router.message(MS_state.ms)
async def handle_text(message: Message, bot: Bot):
