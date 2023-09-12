from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.user.menu import show_my_profile
from keyboards.default.basic import BasicButtons as ButtonsSet
import models
from states.user import UserStates as uStates
import messages


async def get_full_name(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.full_name = msg.text
    await session.commit()
    await msg.answer(messages.ask_sex, reply_markup=ButtonsSet.ask_sex())
    await state.set_state(uStates.waiting_sex)


async def get_sex(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if msg.text in (ButtonsSet.i_am_m, ButtonsSet.i_am_f):
        user.sex = True if msg.text == ButtonsSet.i_am_m else False
        await session.commit()
        await msg.answer(messages.ask_age, reply_markup=ButtonsSet.ask_age(user))
        await state.set_state(uStates.waiting_age)
    else:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_sex())


async def get_age(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.age = int(msg.text)
    try:
        age = int(msg.text)
        if 16 <= age <= 60:
            user.age = age
            await session.commit()
            await msg.answer(messages.ask_location, reply_markup=ButtonsSet.ask_location(user))
            await state.set_state(uStates.waiting_location)
        else:
            raise ValueError
    except ValueError:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_age(user))


async def get_location(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.location = msg.text
    await session.commit()
    await msg.answer(messages.ask_application_type, reply_markup=ButtonsSet.ask_application_type())
    await state.set_state(uStates.waiting_application_type)


async def get_application_type(msg: types.Message, state: FSMContext, session: AsyncSession,
                               user: models.user.User) -> None:
    user.application_type = None
    if msg.text == ButtonsSet.i_have_accomodation:
        user.application_type = int(models.user.ApplicationTypes.has_accomodation)
    elif msg.text == ButtonsSet.i_am_looking_for_accomodation:
        user.application_type = int(models.user.ApplicationTypes.searching_for)
    if user.application_type is not None:
        await session.commit()
        await msg.answer(messages.ask_acceptable_sex, reply_markup=ButtonsSet.ask_acceptable_sex())
        await state.set_state(uStates.waiting_acceptable_sex)
    else:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_application_type())


async def get_acceptable_sex(msg: types.Message, state: FSMContext, session: AsyncSession,
                             user: models.user.User) -> None:
    user.acceptable_sex = None
    if msg.text == ButtonsSet.with_boys:
        user.acceptable_sex = True
    elif msg.text == ButtonsSet.with_girls:
        user.acceptable_sex = False
    elif msg.text == ButtonsSet.with_anyone:
        user.acceptable_sex = None
    if user.acceptable_sex is not None or msg.text == ButtonsSet.with_anyone:
        await session.commit()
        await msg.answer(messages.ask_acceptable_application_type,
                         reply_markup=ButtonsSet.ask_acceptable_application_type())
        await state.set_state(uStates.waiting_acceptable_application_type)
    else:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_acceptable_sex())


async def get_acceptable_application_type(msg: types.Message, state: FSMContext, session: AsyncSession,
                                          user: models.user.User) -> None:
    user.acceptable_application_type = None
    if msg.text == ButtonsSet.with_accomodation:
        user.acceptable_application_type = int(models.user.ApplicationTypes.has_accomodation)
    elif msg.text == ButtonsSet.without_accomodation:
        user.acceptable_application_type = int(models.user.ApplicationTypes.searching_for)
    elif msg.text == ButtonsSet.any:
        user.acceptable_application_type = int(models.user.ApplicationTypes.any)
    if user.acceptable_application_type is not None:
        await session.commit()
        await msg.answer(messages.ask_description, reply_markup=ButtonsSet.ask_description(user))
        await state.set_state(uStates.waiting_description)
    else:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_acceptable_application_type())


async def get_description(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if msg.text != ButtonsSet.leave_as_is:
        user.description = msg.text
    elif user.description is None:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_description(user))
        return
    await session.commit()
    await msg.answer(messages.ask_photos, reply_markup=ButtonsSet.ask_photos())
    await state.set_state(uStates.waiting_photos)


async def get_photos(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if not user.photos:
        user.photos = []
    if msg.text == ButtonsSet.clear:
        user.photos = []
        await session.commit()
        await msg.answer(messages.photos_cleared, reply_markup=ButtonsSet.ask_photos())
    elif msg.text == ButtonsSet.finish and len(list(user.photos)) > 0:
        await show_my_profile(msg, state, user)
    elif msg.photo and len(list(user.photos)) < 5:
        phs = list(user.photos)
        phs.append(msg.photo[-1].file_id)
        user.photos = phs
        await session.commit()
        await msg.answer(messages.photo_added, reply_markup=ButtonsSet.ask_photos())
    else:
        await msg.answer(messages.try_again, reply_markup=ButtonsSet.ask_photos())
