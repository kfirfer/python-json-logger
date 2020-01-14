# coding=utf-8
import inspect
import logging

from custom import util


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
