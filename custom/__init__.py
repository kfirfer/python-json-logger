# coding=utf-8

import logging
import inspect
from custom import util
from custom.util import get_library_logger

_logger = get_library_logger(__name__)
_request_util = None


def init_non_web(**kwargs):
    __init(**kwargs)


def __init(custom_formatter):
    if inspect.isclass(custom_formatter) and issubclass(custom_formatter, logging.Formatter):
        formatter = custom_formatter
        logging._defaultFormatter = formatter()
    else:
        logging._defaultFormatter = custom_formatter

    existing_loggers = list(map(logging.getLogger, logging.Logger.manager.loggerDict))

    if inspect.isclass(custom_formatter) and issubclass(custom_formatter, logging.Formatter):
        formatter = custom_formatter
        util.update_formatter_for_loggers(existing_loggers, formatter)

