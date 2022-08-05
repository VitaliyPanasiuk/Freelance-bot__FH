from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

class getOrder(StatesGroup):
    type = State()
    topic = State()
    comment = State()
    pages = State()
    username = State()