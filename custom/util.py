# coding=utf-8
import random
import string
from logging import Logger


def update_formatter_for_loggers(loggers_iter, formatter):
    for logger in loggers_iter:
        if not isinstance(logger, Logger):
            raise RuntimeError("%s is not a logging.Logger instance", logger)
        for handler in logger.handlers:
            if not isinstance(handler.formatter, formatter):
                handler.formatter = formatter()


def iso_time_format(datetime_):
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (
        datetime_.year, datetime_.month, datetime_.day, datetime_.hour, datetime_.minute, datetime_.second,
        int(datetime_.microsecond / 1000))


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def random_string(size=64):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
