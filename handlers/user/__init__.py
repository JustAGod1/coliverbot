from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter

import states
from filters import ChatTypeFilter

from . import start


def prepare_router() -> Router:
    user_router = Router()
    user_router.message.filter(ChatTypeFilter("private"))

    user_router.message.register(start.deep_link, CommandStart(deep_link_encoded=True))
    user_router.message.register(start.start, CommandStart())
    user_router.message.register(
        start.start, F.text == "🏠В главное меню", StateFilter(states.user.UserStates.menu)
    )
    return user_router
