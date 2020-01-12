import logging
import os
import sys

import custom
from custom.custom_json_format_log import CustomJSONLog


class Logger:
    logger = None

    def __init__(self, log_name):
        custom.init_non_web(custom_formatter=CustomJSONLog)
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger = logger

    def get_logger(self):
        return self.logger


def test_logger():
    logger = Logger("1").get_logger()

    logger.info("test log statement")
    logger.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


def test_logger2():
    os.environ["ELASTICSEARCH_MONITOR_HOSTS"] = "127.0.0.1:9200"
    logger = Logger("2").get_logger()

    logger.info("test log statement")
    logger.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


def test_logger3():
    logger = Logger("3").get_logger()

    logger.info("test log statement")
    logger.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


if __name__ == '__main__':
    # test_logger()
    test_logger2()
    # test_logger3()
