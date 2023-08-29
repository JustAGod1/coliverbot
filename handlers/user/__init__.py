from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

from states.user import UserStates as uStates
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

    m.register(get_details.get_full_name, StateFilter(uStates.waiting_full_name), F.text)
    m.register(get_details.get_sex, StateFilter(uStates.waiting_sex), F.text)
    m.register(get_details.get_age, StateFilter(uStates.waiting_age), F.text)
    m.register(get_details.get_location, StateFilter(uStates.waiting_location), F.text)
    m.register(get_details.get_acceptable_sex, StateFilter(uStates.waiting_acceptable_sex), F.text)
    m.register(get_details.get_acceptable_application_type,
               StateFilter(uStates.waiting_acceptable_application_type), F.text)
    m.register(get_details.get_application_type, StateFilter(uStates.waiting_application_type), F.text)
    m.register(get_details.get_description, StateFilter(uStates.waiting_description), F.text)
    m.register(get_details.get_photos, StateFilter(uStates.waiting_photos), F.text | F.photo)

    m.register(menu.reapply, StateFilter(uStates.menu), F.text == ButtonsSet.menu_reapply)
    m.register(menu.show_my_profile, StateFilter(uStates.menu), F.text == ButtonsSet.menu_show_my_profile)
    m.register(menu.show_opp_profile, StateFilter(uStates.menu), F.text == ButtonsSet.menu_show_opp_profile)

    m.register(menu.like, StateFilter(uStates.scrolling), F.text == ButtonsSet.like)
    m.register(menu.dislike, StateFilter(uStates.scrolling), F.text == ButtonsSet.dislike)
    m.register(menu.sleep, StateFilter(uStates.scrolling), F.text == ButtonsSet.sleep)

    m.register(menu.show_received, StateFilter(uStates.waiting_reveal), F.text == ButtonsSet.show_received)
    m.register(menu.like_liked, StateFilter(uStates.scrolling_received), F.text == ButtonsSet.like)
    m.register(menu.dislike_liked, StateFilter(uStates.scrolling_received), F.text == ButtonsSet.dislike)

    return user_router
