from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

class getOrder(StatesGroup):
    type = State()
    new_type = State()
    topic = State()
    comment = State()
    pages = State()
    username = State()
    answer = State()
    author_id = State()
    
    
class private_get(StatesGroup):
    money = State()
    
class mailing(StatesGroup):
    get_teamlead = State()
    get_answer = State()
    get_author = State()
    get_author_private = State()
    get_order_id = State()
class reg_author(StatesGroup):
    get_card = State()
    get_speciality = State()