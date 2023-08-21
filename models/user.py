import enum
import uuid as python_uuid
import datetime
import pytz
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy import Integer, BigInteger, String, Uuid, DateTime, Enum, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from aiogram.types import TelegramObject

from .base import Base


# from pydantic import BaseModel, ConfigDict, constr


class Platforms(enum.Enum):
    undefined = 0
    console = 1
    telegram = 2
    vk = 3


class ApplicationTypes(enum.Enum):
    undefined = 0
    has_accomodation = 1
    searching_for = 2
    both_and_nothing = 3


# sqlalchemy model
class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[python_uuid.UUID] = mapped_column(Uuid, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(32))
    refer: Mapped[Optional[str]] = mapped_column(String(50))
    platform: Mapped[Platforms] = mapped_column(Enum(Platforms), nullable=False)
    platform_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_access_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    sex: Mapped[Optional[bool]] = mapped_column(Boolean)
    age: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    location: Mapped[Optional[str]] = mapped_column(String(70), index=True)  # assuming locations are common
    acceptable_sex: Mapped[Optional[bool]] = mapped_column(Boolean)
    acceptable_application_type: Mapped[Optional[ApplicationTypes]] = mapped_column(Enum(ApplicationTypes))
    application_type: Mapped[Optional[ApplicationTypes]] = mapped_column(Enum(ApplicationTypes))
    description: Mapped[Optional[str]] = mapped_column(Text)
    photos: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String(255)))  # TODO: check if more than 3/10?


async def get_or_create(session: AsyncSession, event: TelegramObject) -> User:
    statement = select(User).where(User.platform.is_(Platforms.telegram).and_(User.platform_id.is_(event.from_user.id)))
    result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            uuid=python_uuid.uuid4(),
            username=event.from_user.username,
            platform=Platforms.telegram,
            platform_id=event.from_user.id,
            start_time=datetime.datetime.now(pytz.timezone('Europe/Moscow')),
            last_access_time=datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        )
        session.add(user)
        await session.commit()
    return user

# pydantic model
# class User(BaseModel):
#     uuid: python_uuid.UUID
#     username: Optional[str]
#     refer: Optional[str]
#     platform: Platforms
#     platform_id: int
#     start_time: datetime.datetime
#     last_access_time: datetime.datetime
#
#     full_name: Optional[str]
#     sex: Optional[bool]
#     age: Optional[int]
#     location: Optional[str]
#     acceptable_sex: Optional[bool]
#     acceptable_application_type: Optional[ApplicationTypes]
#     application_type: Optional[ApplicationTypes]
#     description: Optional[str]
#     photos: Optional[List[str]]  # TODO: check if more than 3/10?
