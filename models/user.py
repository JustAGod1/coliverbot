import enum
import random
import uuid as python_uuid
import datetime
import pytz
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy import Integer, BigInteger, String, Uuid, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


# from pydantic import BaseModel, ConfigDict, constr


class Platforms(enum.IntEnum):
    undefined = 0
    console = 1
    telegram = 2
    vk = 3


class ApplicationTypes(enum.IntEnum):
    undefined = 0
    has_accomodation = 1
    searching_for = 2
    any = 3


class UserStatuses(enum.IntEnum):
    undefined = 0
    active = 1
    inactive = 2
    paused = 3
    banned = 4


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[python_uuid.UUID] = mapped_column(Uuid, primary_key=True, default=python_uuid.uuid4)
    username: Mapped[Optional[str]] = mapped_column(String(32))
    refer: Mapped[Optional[str]] = mapped_column(String(50))
    platform: Mapped[int] = mapped_column(Integer, nullable=False)
    platform_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_access_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    sex: Mapped[Optional[bool]] = mapped_column(Boolean)
    age: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(70), index=True)  # assuming locations are common
    application_type: Mapped[Optional[int]] = mapped_column(Integer)
    acceptable_sex: Mapped[Optional[bool]] = mapped_column(Boolean)
    acceptable_application_type: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String(255)))
    status: Mapped[int] = mapped_column(Integer, nullable=False)


async def get_or_create(session: AsyncSession, tgid: int) -> User:
    statement = (select(User)
                 .where(User.platform == int(Platforms.telegram))
                 .where(User.platform_id == tgid)
                 )
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            platform=Platforms.telegram,
            platform_id=tgid,
            # TODO: for some reason time in db is without timezone
            start_time=datetime.datetime.now(pytz.timezone('Europe/Moscow')),
            last_access_time=datetime.datetime.now(pytz.timezone('Europe/Moscow')),
            status=UserStatuses.inactive
        )
        session.add(user)
    else:
        user.last_access_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    await session.commit()
    return user


async def get_random(session: AsyncSession, user: User) -> User:
    statement = (select(User)
                 .where(User.platform == int(Platforms.telegram))
                 .where(User.platform_id != user.platform_id)
                 )
    result = await session.execute(statement)
    users = result.scalars().all()
    return random.choice(users)


async def get_by_uuid(session: AsyncSession, uuid: python_uuid.UUID) -> User:
    statement = (select(User)
                 .where(User.uuid == uuid)
                 )
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    return user
