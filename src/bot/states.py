from aiogram.fsm.state import State, StatesGroup

class CreateTestFSM(StatesGroup):
    """Стейт для создания теста"""
    topic = State()
    preview = State()
    revision = State()
    
class PassTestFSM(StatesGroup):
    """Стейт для прохождения теста"""
    waiting_fullname = State()