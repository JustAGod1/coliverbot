import enum
import uuid as python_uuid
import datetime
import pytz
from typing import Optional
from sqlalchemy import select, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

import models.user
from .base import Base


class RelationTypes(enum.IntEnum):
    undefined = 0
    like = 1
    match = 2
    dislike = 3
    reject = 4
    shown = 5


class Relation(Base):
    __tablename__ = 'relations'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    from_uuid: Mapped[python_uuid.UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False, index=True)
    to_uuid: Mapped[python_uuid.UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False, index=True)
    relation_type: Mapped[int] = mapped_column(Integer, nullable=False)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)


async def create(session: AsyncSession, from_user: models.user.User, to_user: models.user.User, relation: int) -> None:
    relation = Relation(
        from_uuid=from_user.uuid,
        to_uuid=to_user.uuid,
        relation_type=relation,
        # TODO: for some reason time in db is without timezone
        creation_time=datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    )
    session.add(relation)
    await session.commit()


async def get_oldest_like_to(session: AsyncSession, user: models.user.User) -> Optional[Relation]:
    statement = (select(Relation)
                 .where(Relation.to_uuid == user.uuid)
                 .where(Relation.relation_type == int(RelationTypes.like))
                 .order_by(Relation.creation_time.desc())
                 .limit(1)
                 )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_by_id(session: AsyncSession, i: int) -> Optional[Relation]:
    statement = (select(Relation)
                 .where(Relation.id == i)
                 )
    result = await session.execute(statement)
    return result.scalar_one_or_none()
