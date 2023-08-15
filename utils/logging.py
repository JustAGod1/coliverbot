import logging
import sys

import structlog

import models
from . import config


def setup_logger() -> structlog.typing.FilteringBoundLogger:
    logging.basicConfig(
        level=config.LOGGING_LEVEL,
        stream=sys.stdout,
    )
    log: structlog.typing.FilteringBoundLogger = structlog.get_logger(
        structlog.stdlib.BoundLogger
    )
    shared_processors: list[structlog.typing.Processor] = [
        structlog.processors.add_log_level
    ]
    processors = shared_processors + [
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.dev.ConsoleRenderer(),
    ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(config.LOGGING_LEVEL),
    )
    return log
