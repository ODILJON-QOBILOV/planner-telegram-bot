from aiogram.dispatcher.filters.state import State, StatesGroup


class Add_Plan(StatesGroup):
    plan = State()


class Plan_id(StatesGroup):
    pk = State()

class Edit_Plan(StatesGroup):
    pk = State()
    edited_plan = State()
    edited_status = State()

class Save_Up(StatesGroup):
    money = State()