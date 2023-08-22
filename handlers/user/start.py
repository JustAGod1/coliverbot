from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import models
import states
import messages


async def start(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    await msg.answer(messages.greeting)
    if user.photos:
        await msg.answer(messages.menu)
        await state.set_state(states.user.UserStates.menu)
    else:
        await msg.answer(messages.ask_full_name)
        await state.set_state(states.user.UserStates.waiting_full_name)


# async def deep_link(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
#     user.refer = msg.get_args().split("_")[1]
#     await session.commit()
#     await start(msg, state, session, user)
