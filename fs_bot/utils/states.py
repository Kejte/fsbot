from aiogram.fsm.state import StatesGroup, State

class AddGroupState(StatesGroup):
    GET_TITLE = State()
    GET_SUBJECT = State()
    GET_RESULT = State()


class AddMediaState(StatesGroup):
    GET_MEDIA = State()