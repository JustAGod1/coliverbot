from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

import states
from filters import ChatTypeFilter
from keyboards.default.basic import BasicButtons as ButtonsSet

from . import start
from . import get_details
from . import menu


def prepare_router() -> Router:
    user_router = Router()
    m = user_router.message
    m.filter(ChatTypeFilter("private"))

    # user_router.message.register(start.deep_link, CommandStart(deep_link_encoded=True))
    m.register(start.start, CommandStart())

    m.register(get_details.get_full_name,
               StateFilter(states.user.UserStates.waiting_full_name), F.text)
    m.register(get_details.get_sex,
               StateFilter(states.user.UserStates.waiting_sex), F.text)
    m.register(get_details.get_age,
               StateFilter(states.user.UserStates.waiting_age), F.text)
    m.register(get_details.get_location,
               StateFilter(states.user.UserStates.waiting_location), F.text)
    m.register(get_details.get_acceptable_sex,
               StateFilter(states.user.UserStates.waiting_acceptable_sex), F.text)
    m.register(get_details.get_acceptable_application_type,
               StateFilter(states.user.UserStates.waiting_acceptable_application_type), F.text)
    m.register(get_details.get_application_type,
               StateFilter(states.user.UserStates.waiting_application_type), F.text)
    m.register(get_details.get_description,
               StateFilter(states.user.UserStates.waiting_description), F.text)
    m.register(get_details.get_photos,
               StateFilter(states.user.UserStates.waiting_photos), F.text | F.photo)

    m.register(menu.reapply,
               StateFilter(states.user.UserStates.menu), F.text == ButtonsSet.menu_reapply)
    m.register(menu.show_my_profile,
               StateFilter(states.user.UserStates.menu), F.text == ButtonsSet.menu_show_my_profile)
    m.register(menu.show_opp_profile,
               StateFilter(states.user.UserStates.menu), F.text == ButtonsSet.menu_show_opp_profile)

    m.register(menu.like,
               StateFilter(states.user.UserStates.scrolling), F.text == ButtonsSet.like)
    m.register(menu.dislike,
               StateFilter(states.user.UserStates.scrolling), F.text == ButtonsSet.dislike)
    m.register(menu.sleep,
               StateFilter(states.user.UserStates.scrolling), F.text == ButtonsSet.sleep)

    return user_router
