import asyncio

from aiogram import Dispatcher, Bot

import asyncpg
import structlog
import tenacity
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from tenacity import _utils
import orjson

import utils
import handlers
from middlewares import StructLoggingMiddleware

TIMEOUT_BETWEEN_ATTEMPTS = 2
MAX_TIMEOUT = 30


def before_log(retry_state: tenacity.RetryCallState) -> None:
    if retry_state.outcome is None:
        return
    if retry_state.outcome.failed:
        verb, value = "raised", retry_state.outcome.exception()
    else:
        verb, value = "returned", retry_state.outcome.result()
    logger = retry_state.kwargs["logger"]
    logger.info(
        "Retrying {callback} in {sleep} seconds as it {verb} {value}".format(
            callback=_utils.get_callback_name(retry_state.fn),  # type: ignore
            sleep=retry_state.next_action.sleep,  # type: ignore
            verb=verb,
            value=value,
        ),
        callback=_utils.get_callback_name(retry_state.fn),  # type: ignore
        sleep=retry_state.next_action.sleep,  # type: ignore
        verb=verb,
        value=value,
    )


def after_log(retry_state: tenacity.RetryCallState) -> None:
    logger = retry_state.kwargs["logger"]
    logger.info(
        "Finished call to {callback!r} after {time:.2f}, this was the {attempt} time calling it.".format(
            callback=_utils.get_callback_name(retry_state.fn),  # type: ignore
            time=retry_state.seconds_since_start,
            attempt=_utils.to_ordinal(retry_state.attempt_number),
        ),
        callback=_utils.get_callback_name(retry_state.fn),  # type: ignore
        time=retry_state.seconds_since_start,
        attempt=_utils.to_ordinal(retry_state.attempt_number),
    )


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)
async def wait_postgres(
        logger: structlog.typing.FilteringBoundLogger,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
) -> asyncpg.Pool:
    db_pool: asyncpg.Pool = await asyncpg.create_pool(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        min_size=1,
        max_size=3,
    )
    version = await db_pool.fetchrow("SELECT version() as ver;")
    logger.debug("Connected to PostgreSQL.", version=version["ver"])
    return db_pool


async def create_db_connections(dp: Dispatcher) -> None:
    logger: structlog.typing.FilteringBoundLogger = dp["business_logger"]

    logger.debug("Connecting to PostgreSQL", db="main")
    try:
        db_pool = await wait_postgres(
            logger=dp["db_logger"],
            host=utils.config.PG_HOST,
            port=utils.config.PG_PORT,
            user=utils.config.PG_USER,
            password=utils.config.PG_PASSWORD,
            database=utils.config.PG_DATABASE,
        )
    except tenacity.RetryError:
        logger.error("Failed to connect to PostgreSQL", db="main")
        exit(1)
    else:
        logger.debug("Succesfully connected to PostgreSQL", db="main")
    dp["db_pool"] = db_pool


async def close_db_connections(dp: Dispatcher) -> None:
    if "db_pool" in dp.workflow_data:
        db_pool: asyncpg.Pool = dp["db_pool"]
        await db_pool.close()


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logging.setup_logger().bind(type="aiogram")
    dp["db_logger"] = utils.logging.setup_logger().bind(type="db")
    dp["business_logger"] = utils.logging.setup_logger().bind(type="business")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await create_db_connections(dp)
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await close_db_connections(dispatcher)
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
