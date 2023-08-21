from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

import models


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if "session" in data:
            # if isinstance(event, (Message, CallbackQuery)):

            if event.event.from_user.id is None:
                return await handler(event, data)
            session: AsyncSession = data["session"]
            user = await models.user.get_or_create(session, event.event.from_user.id)
            data["user"] = user
            return await handler(event, data)
