from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import models
import states
import messages


async def get_full_name(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.full_name = msg.text
    await session.commit()
    await msg.answer(messages.ask_sex)
    await state.set_state(states.user.UserStates.waiting_sex)


async def get_sex(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.sex = True if msg.text == "Мужской" else False  # TODO: add validation
    await session.commit()
    await msg.answer(messages.ask_age)
    await state.set_state(states.user.UserStates.waiting_age)


async def get_age(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.age = int(msg.text)  # TODO: add validation
    await session.commit()
    await msg.answer(messages.ask_location)
    await state.set_state(states.user.UserStates.waiting_location)


async def get_location(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.location = msg.text
    await session.commit()
    await msg.answer(messages.ask_application_type)
    await state.set_state(states.user.UserStates.waiting_application_type)


async def get_application_type(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    if msg.text == "Уже есть жилье":  # TODO: bind to keyboard buttons
        user.application_type = int(models.user.ApplicationTypes.has_accomodation)
    elif msg.text == "Хочу заселиться":
        user.application_type = int(models.user.ApplicationTypes.searching_for)
    await session.commit()
    await msg.answer(messages.ask_acceptable_sex)
    await state.set_state(states.user.UserStates.waiting_acceptable_sex)


async def get_acceptable_sex(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.acceptable_sex = True if msg.text == "Мужской" else None
    user.acceptable_sex = False if msg.text == "Женский" else None
    # if msg.text == "Любой": # TODO: add validation
    if user.acceptable_sex is not None:
        await session.commit()
    await msg.answer(messages.ask_acceptable_application_type)
    await state.set_state(states.user.UserStates.waiting_acceptable_application_type)


async def get_acceptable_application_type(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.acceptable_application_type = True if msg.text == "Приложение" else False  # TODO: add validation
    await session.commit()
    await msg.answer(messages.ask_description)
    await state.set_state(states.user.UserStates.waiting_description)


async def get_description(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:
    user.description = msg.text
    await session.commit()
    await msg.answer(messages.ask_photos)
    await state.set_state(states.user.UserStates.waiting_photos)


async def get_photos(msg: types.Message, state: FSMContext, session: AsyncSession, user: models.user.User) -> None:

    await msg.answer("Спасибо за регистрацию!")
    await state.finish()
