from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.default.basic import BasicButtons as ButtonsSet
import models
import states
import messages


async def reapply(msg: types.Message, state: FSMContext, user: models.user.User) -> None:
    await msg.answer(messages.ask_full_name, reply_markup=ButtonsSet.ask_full_name(user))
    await state.set_state(states.user.UserStates.waiting_full_name)


async def show_my_profile(msg: types.Message, state: FSMContext, user: models.user.User) -> None:
    # TODO: refactor this
    media = list()
    media.append(types.InputMediaPhoto(media=str(user.photos[0]), caption=messages.profile(user)))
    for photo in user.photos[1:]:
        media.append(types.InputMediaPhoto(media=str(photo)))
    await msg.answer_media_group(media)
    await msg.answer(messages.menu, reply_markup=ButtonsSet.menu())
    await state.set_state(states.user.UserStates.menu)


async def show_opp_profile(msg: types.Message, state: FSMContext, session: AsyncSession,
                           user: models.user.User) -> None:
    if msg.text == ButtonsSet.menu_show_opp_profile:
        await msg.answer(messages.show_opp_placeholder, reply_markup=ButtonsSet.scrolling())
    opp_user = await models.user.get_random(session, user)
    media = list()
    media.append(types.InputMediaPhoto(media=str(opp_user.photos[0]), caption=messages.profile(opp_user)))
    for photo in opp_user.photos[1:]:
        media.append(types.InputMediaPhoto(media=str(photo)))
    await msg.answer_media_group(media)
    await state.set_state(states.user.UserStates.scrolling)


async def like(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    # TODO: add like
    await msg.answer(messages.like)
    await show_opp_profile(msg, state, session, user)


async def dislike(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    await show_opp_profile(msg, state, session, user)


async def sleep(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(messages.sleep)
    await msg.answer(messages.menu, reply_markup=ButtonsSet.menu())
    await state.set_state(states.user.UserStates.menu)
