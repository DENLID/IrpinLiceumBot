from aiogram.fsm.state import StatesGroup, State

class Communication(StatesGroup):
    mess = State()

class RegisterStudent(StatesGroup):
    email = State()
    fullname = State()
    birth_certificate = State()

class MS_state(StatesGroup):
    students_number = State()
    ms_number = State()
    ms_number_hv = State()
    ms = State()

class ConfirmPerson(StatesGroup):
    email = State()
    phone = State()