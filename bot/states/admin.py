from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    sticker_data = State()
    sticker_name = State()
