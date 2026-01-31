from aiogram.fsm.state import State, StatesGroup

class CreateTestFSM(StatesGroup):
    """Стейт для создания теста"""
    topic = State()
    count = State()
    preview = State()
    
class PassTestFSM(StatesGroup):
    """Стейт для прохождения теста"""
    waiting_fullname = State()