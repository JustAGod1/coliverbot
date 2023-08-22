from aiogram import Router, types
from filters import ChatTypeFilter

import messages


async def undefined(msg: types.Message) -> None:
    await msg.answer(messages.undefined)


def prepare_router() -> Router:
    undefined_router = Router()
    m = undefined_router.message
    m.filter(ChatTypeFilter("private"))
    m.register(undefined)
    return undefined_router
