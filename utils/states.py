from aiogram.fsm.state import StatesGroup, State

class Communication(StatesGroup):
    mess = State()

class RegisterStudent(StatesGroup):
    email = State()
    fullname = State()
    birth_certificate = State()