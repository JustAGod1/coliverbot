import asyncio

import sqlalchemy
from aiogram import Dispatcher, Bot

import orjson
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from models.base import Base
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import utils
import handlers
from middlewares import StructLoggingMiddleware, DbSessionMiddleware, UserMiddleware


async def connect_db(dp: Dispatcher) -> None:
    db_engine = create_async_engine(utils.config.DB_URL, echo=True)
    with db_engine.connect() as conn:
        Base.metadata.create_all(conn)
    sessionmaker = async_sessionmaker(db_engine, expire_on_commit=False)

    async with db_engine.begin() as conn:
        await conn.run_sync(MetaData().create_all)

    dp["db_engine"] = db_engine
    dp["sessionmaker"] = sessionmaker


async def close_db(dp: Dispatcher) -> None:
    if "db_engine" in dp.workflow_data:
        db_engine: sqlalchemy.ext.asyncio.AsyncEngine = dp["db_engine"]
        await db_engine.dispose()


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))
    dp.update.middleware(DbSessionMiddleware(session_pool=dp["sessionmaker"]))
    dp.update.middleware(UserMiddleware())


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger().bind(type="aiogram")
    dp["db_logger"] = utils.logging.setup_logger().bind(type="db")
    dp["business_logger"] = utils.logging.setup_logger().bind(type="business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await connect_db(dp)
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await close_db(dispatcher)
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


def main() -> None:
    session = AiohttpSession(json_loads=orjson.loads)
    bot = Bot(utils.config.BOT_TOKEN, parse_mode="HTML", session=session)

    dp = Dispatcher(
        storage=RedisStorage(
            redis=Redis(
                host=utils.config.FSM_HOST,
                password=utils.config.FSM_PASSWORD,
                port=utils.config.FSM_PORT,
                db=0,
            ),
        )
    )

    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
