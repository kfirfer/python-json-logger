import os
import time

import custom
import sys
import logging
from custom.custom_json_format_log import CustomJSONLog
from custom.custom_plain_format_log import CustomPlainLog


class Logger:
    logger = None

    def __init__(self, s):
        if s == "1":
            formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
            custom.init_non_web(custom_formatter=formatter)
        elif s == "2":
            custom.init_non_web(custom_formatter=CustomJSONLog)
        else:
            custom.init_non_web(custom_formatter=CustomPlainLog)

        logger = logging.getLogger(s)
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
    # time.sleep(5)
    # test_logger3()
