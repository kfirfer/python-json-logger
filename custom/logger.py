import custom
import sys
import logging
from custom.custom_json_format_log import CustomJSONLog


class Logger:
    logger = None

    def __init__(self, s):
        if s == "1":
            formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
            custom.init_non_web(custom_formatter=formatter)
        else:
            custom.init_non_web(custom_formatter=CustomJSONLog)

        logger = logging.getLogger(s)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger = logger

    def get_logger(self):
        return self.logger


def test_logger():
    logger = Logger("0").get_logger()

    logger.info("test log statement")
    logger.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


def test_logger2():
    logger = Logger("1").get_logger()

    logger.info("test log statement")
    logger.info("test log statement", extra={'props': {"extra_property": 'extra_value'}})


if __name__ == '__main__':
    test_logger()
    test_logger2()
