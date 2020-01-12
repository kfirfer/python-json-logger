import logging
import os
import sys

import custom
from custom.custom_json_format_log import CustomJSONLog


def logger(log_name):
    custom.init_non_web(custom_formatter=CustomJSONLog)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


def test_logger1():
    os.environ["ELASTICSEARCH_MONITOR_HOSTS"] = "127.0.0.1:9200"
    log = logger("1")
    log.info("test log statement")
    log.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


def test_logger2():
    log = logger("2")
    log.info("test log statement")
    log.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


def test_logger3():
    log = logger("3")
    try:
        print(0 / 0)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    test_logger1()
    test_logger2()
    test_logger3()
