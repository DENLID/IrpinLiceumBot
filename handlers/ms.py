from aiogram.types import Message
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from utils.states import Communication
from filters.filters import IsAdminChat, IsWadMessage, IsMsAdmin
import keyboards.keyboards as keyboards
import config


router = Router()

