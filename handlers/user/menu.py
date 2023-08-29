from typing import List

import aiogram
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

import models.relation
from keyboards.default.basic import BasicButtons as ButtonsSet
import models
from states.user import UserStates as uStates
import messages


async def reapply(msg: types.Message, state: FSMContext, user: models.user.User) -> None:
    await msg.answer(messages.ask_full_name, reply_markup=ButtonsSet.ask_full_name(user))
    await state.set_state(uStates.waiting_full_name)


def _media(user: models.user.User, received_like: bool = False) -> List[InputMediaPhoto]:
    media = list()
    caption: str = ''
    if received_like:
        caption += messages.you_were_liked
    caption += messages.profile(user)
    media.append(types.InputMediaPhoto(media=str(user.photos[0]), caption=caption))
    for photo in user.photos[1:]:
        media.append(types.InputMediaPhoto(media=str(photo)))
    return media


async def show_my_profile(msg: types.Message, state: FSMContext, user: models.user.User) -> None:
    await msg.answer_media_group(_media(user))
    await msg.answer(messages.menu, reply_markup=ButtonsSet.menu())
    await state.set_state(uStates.menu)


async def show_opp_profile(msg: types.Message, state: FSMContext, session: AsyncSession,
                           user: models.user.User) -> None:
    if msg.text == ButtonsSet.menu_show_opp_profile:
        await msg.answer(messages.kb_placeholder, reply_markup=ButtonsSet.scrolling())
    user_to_be_shown = await models.user.get_random(session, user)
    await msg.answer_media_group(_media(user_to_be_shown))
    await state.update_data(showed_user_uuid=str(user_to_be_shown.uuid))
    await state.set_state(uStates.scrolling)


async def like(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User,
               bot: aiogram.Bot, dispatcher: aiogram.Dispatcher) -> None:
    # TODO: check platform, check that recepient is not blocked
    data = await state.get_data()
    showed_user: models.user.User = await models.user.get_by_uuid(session, data['showed_user_uuid'])
    await bot.send_message(showed_user.platform_id, messages.ask_reveal, reply_markup=ButtonsSet.ask_reveal())
    showed_user_state = dispatcher.fsm.resolve_context(bot=bot, chat_id=showed_user.platform_id,
                                                       user_id=showed_user.platform_id)  # TODO: when is it none?
    await showed_user_state.set_state(uStates.waiting_reveal)
    await models.relation.create(session, user, showed_user, models.relation.RelationTypes.like)
    await msg.answer(messages.you_liked)
    await show_opp_profile(msg, state, session, user)


async def dislike(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    data = await state.get_data()
    showed_user: models.user.User = await models.user.get_by_uuid(session, data['showed_user_uuid'])
    await models.relation.create(session, user, showed_user, models.relation.RelationTypes.dislike)
    await show_opp_profile(msg, state, session, user)


async def sleep(msg: types.Message, state: FSMContext) -> None:
    await msg.answer(messages.sleep)
    # TODO: implement sleep/pause
    await msg.answer(messages.menu, reply_markup=ButtonsSet.menu())
    await state.set_state(uStates.menu)


async def show_received(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if msg.text == ButtonsSet.show_received:
        await msg.answer(messages.kb_placeholder, reply_markup=ButtonsSet.scrolling_received())
    relation = await models.relation.get_oldest_like_to(session, user)
    if relation is None:
        return await show_my_profile(msg, state, user)
    user_to_be_shown = await models.user.get_by_uuid(session, relation.from_uuid)
    await msg.answer_media_group(_media(user_to_be_shown, received_like=True))
    await state.update_data(showed_relation_id=relation.id)
    await state.set_state(uStates.scrolling_received)


async def _state_to_showed_relation(state: FSMContext, session: AsyncSession) -> models.relation.Relation:
    data = await state.get_data()
    return await models.relation.get_by_id(session, int(data['showed_relation_id']))


async def like_liked(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    showed_relation: models.relation.Relation = await _state_to_showed_relation(state, session)
    showed_relation.relation_type = models.relation.RelationTypes.match
    await session.commit()
    showed_user: models.user.User = await models.user.get_by_uuid(session, showed_relation.from_uuid)
    await msg.answer(messages.you_matched(showed_user.username))
    await show_received(msg, state, session, user)


async def dislike_liked(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    showed_relation: models.relation.Relation = await _state_to_showed_relation(state, session)
    showed_relation.relation_type = models.relation.RelationTypes.reject
    await session.commit()
    await show_received(msg, state, session, user)
