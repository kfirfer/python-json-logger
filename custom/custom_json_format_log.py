# This example shows how the logger can be set up to use a custom JSON format.
import json
import logging
import traceback
from datetime import datetime

from custom import util


JSON_SERIALIZER = lambda log: json.dumps(log, ensure_ascii=False)


def _sanitize_log_msg(record):
    return record.getMessage().replace('\n', '_').replace('\r', '_').replace('\t', '_')


class CustomJSONLog(logging.Formatter):
    """
    Formatter for web application log
    """
    elastic_search_logger = None

    def __init__(self):
        super().__init__()
        from custom.loggers import ElasticSearchLogger
        self.elastic_search_logger = ElasticSearchLogger()

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {
            'exc_info': exc_info,
            'filename': record.filename,
        }

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):
        utcnow = datetime.utcnow()
        json_log_object = {"type": "log",
                           "logger": record.name,
                           "thread": record.threadName,
                           "level": record.levelname,
                           "module": record.module,
                           "line_no": record.lineno,
                           "message": _sanitize_log_msg(record)
                           }

        if hasattr(record, 'props'):
            json_log_object.update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object.update(self.get_exc_fields(record))

        json_log_object['date'] = util.iso_time_format(utcnow)

        # for key, value in tags.items():
        #     body[key] = value
        #
        # for key, value in self.kwargs.items():
        #     body[key] = value
        #
        # for key, value in kwargs.items():
        #     body[key] = value

        self.elastic_search_logger.external_logger(body=json_log_object)

        return JSON_SERIALIZER(json_log_object)
