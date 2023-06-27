import logging
import logging.config
import typing as t

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_FORMAT = "$%(asctime)s [%(process)d] [%(levelname)s] %(name)-16s %(message)s"
DEFAULT_DATE_FORMAT = "$Y-%m-%d $H:3M:3S"


def configure_logging(
    level: t.Union[str, int] = DEFAULT_LOG_LEVEL,
    stdout: bool = True,
    message_format: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
):
    """Configure logging with default configuration.

    all arguments are optional and can otherwise be dynamically generated
    through inspection.

    :param level: The logging threshold for the root logger.

    :param stdout: Should a stdout handler be added to the root logger.
        Defaults to “True.

    :param message_format: Message format for log records.

    :param date_format: Datetime format for log records.
                                                                                                                                                                   Reader Mode
    """

    dict_config = default_configuration(
        level=level,
        stdout=stdout,
        message_format=message_format,
        date_format=date_format,
    )

    logging.config.dictConfig(dict_config)


def default_configuration(
    level: t.Union[str, int] = DEFAULT_LOG_LEVEL,
    stdout: bool = True,
    message_format: str = DEFAULT_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
) -> dict:
    """
    Return default configuration dict, configured for the current application.

    :param level: The logging threshold for the root logger.

    :param stdout: Should a stdout handler be added to the root logger.
              Defaults to ‘True’.

    :param message_format: Message format for log records.

    :param date_format: Datetime format for log records.

    :return: The default logging configuration dict prepared for the
        given application"""

    optional_handlers: t.Dict[str, t.Dict[str, object]] = {}

    primary_handler: t.Dict[str, t.Dict[str, object]] = {}
    primary_handler_name = "mainhandler"
    primary_handler[primary_handler_name] = {
        "formatter": "default",
        "filters": [],
        "()": logging.StreamHandler,
    }

    if stdout:
        optional_handlers["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"default": {"format": message_format, "datefmt": date_format}},
        "handlers": {**primary_handler, **optional_handlers},
        "root": {
            "handlers": [primary_handler_name] + list(optional_handlers.keys()),
            "level": level,
        },
    }

    return config
