from aiogram.fsm.state import StatesGroup, State

class AddGroupState(StatesGroup):
    GET_TITLE = State()
    GET_MEMBERS = State()
    GET_RESULT = State()


class AddSubjectsState(StatesGroup):
    GET_SUBJECTS = State()