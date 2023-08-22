from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import models
import states
import messages


async def reapply(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    await msg.answer(messages.ask_full_name)
    await state.set_state(states.user.UserStates.waiting_full_name)


async def show_my_profile(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    await msg.answer_photo(str(user.photos[0]), caption=messages.my_profile(user))
    await msg.answer(messages.menu)
    await state.set_state(states.user.UserStates.menu)


async def show_profiles(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    pass  # TODO: scrollig
