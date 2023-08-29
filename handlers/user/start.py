from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.default.basic import BasicButtons as ButtonsSet
import models
from states.user import UserStates as uStates
import messages


async def start(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if not user.refer and msg.text.split()[1:]:
        user.refer = msg.text.split()[1]
        await session.commit()

    await msg.answer(messages.greeting)
    if user.photos:
        await msg.answer(messages.menu, reply_markup=ButtonsSet.menu())
        await state.set_state(uStates.menu)
    else:
        await msg.answer(messages.ask_full_name, reply_markup=ButtonsSet.ask_full_name(user))
        await state.set_state(uStates.waiting_full_name)
