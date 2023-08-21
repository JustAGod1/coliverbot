from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

import states
from filters import ChatTypeFilter

from . import start
from . import get_details


def prepare_router() -> Router:
    user_router = Router()
    m = user_router.message
    m.filter(ChatTypeFilter("private"))

    # user_router.message.register(start.deep_link, CommandStart(deep_link_encoded=True))
    m.register(start.start, CommandStart())
    m.register(get_details.get_full_name, StateFilter(states.user.UserStates.waiting_full_name))
    m.register(get_details.get_sex, StateFilter(states.user.UserStates.waiting_sex))
    m.register(get_details.get_age, StateFilter(states.user.UserStates.waiting_age))
    m.register(get_details.get_location, StateFilter(states.user.UserStates.waiting_location))
    m.register(get_details.get_acceptable_sex, StateFilter(states.user.UserStates.waiting_acceptable_sex))
    m.register(get_details.get_acceptable_application_type, StateFilter(states.user.UserStates.waiting_acceptable_application_type))
    m.register(get_details.get_application_type, StateFilter(states.user.UserStates.waiting_application_type))
    m.register(get_details.get_description, StateFilter(states.user.UserStates.waiting_description))


    user_router.message.register(
        start.start, F.text == "🏠В главное меню", StateFilter(states.user.UserStates.menu)
    )
    return user_router
