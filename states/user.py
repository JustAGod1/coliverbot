from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    undefined = State()
    waiting_full_name = State()
    waiting_sex = State()
    waiting_age = State()
    waiting_location = State()
    waiting_acceptable_sex = State()
    waiting_acceptable_application_type = State()
    waiting_application_type = State()
    waiting_description = State()
    waiting_photos = State()
    menu = State()
    # wainting_for_pause_confirm = State()
    # paused = State()
    scrolling = State()
    # waiting_reveal = State()
    # scrolling_received = State()
