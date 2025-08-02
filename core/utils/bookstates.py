from aiogram.fsm.state import StatesGroup, State

class StepsFormBook(StatesGroup):
    GET_ID_LIST = State()
    GET_NAME_BOOK = State()
    GET_LINK_BOOK = State()