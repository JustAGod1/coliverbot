from aiogram import html, types
from aiogram.fsm.context import FSMContext

import states
import messages


async def start(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(messages.greeting)
    await state.set_state(states.user.UserMainMenu.menu)

async def start_with_deep_link(msg: types.Message, state: FSMContext) -> None:

