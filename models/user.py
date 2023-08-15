from .base import BaseModel

import enum
import uuid
import datetime
from typing import List
from sqlalchemy import Column, Integer, BigInteger, String, Uuid, DateTime, Enum, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import ConfigDict, constr

Base = declarative_base()


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


class UserOrm(Base):
    __tablename__ = 'users'

    uuid = Column(Uuid, primary_key=True)
    username = Column(String(32))
    refer = Column(String(50))
    platform = Column(Enum(Platforms), nullable=False)
    platform_id = Column(BigInteger, nullable=False)
    start_time = Column(DateTime, nullable=False)
    last_access_time = Column(DateTime, nullable=False)

    full_name = Column(String(100))
    sex = Column(Boolean)
    age = Column(Integer, index=True)
    location = Column(String(70), index=True)
    acceptable_sex = Column(Boolean)
    acceptable_application_type = Column(Enum(ApplicationTypes))
    application_type = Column(Enum(ApplicationTypes))
    description = Column(Text)
    photos = Column(ARRAY(String(255)))  # TODO: check if more than 3/10?


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: uuid.UUID
    usename: constr(max_length=32)
    refer: constr(max_length=50)
    platform: Platforms
    platform_id: int
    start_time: datetime.datetime
    last_access_time: datetime.datetime

    full_name: constr(max_length=100)
    sex: bool
    age: int
    location: constr(max_length=70)
    acceptable_sex: bool
    acceptable_application_type: ApplicationTypes
    application_type: ApplicationTypes
    description: str
    photos: List[constr(max_length=255)]
