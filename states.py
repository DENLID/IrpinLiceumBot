from aiogram.fsm.state import StatesGroup, State

class Communication(StatesGroup):
    mess = State()
    wad_state = State()
    news_state = State()
