# This example shows how the logger can be set up to use a custom JSON format.
import json
import logging
import os
import traceback
from datetime import datetime

from custom import util


def json_serializer(log):
    return json.dumps(log, ensure_ascii=False)


def _sanitize_log_msg(record):
    return record.getMessage().replace('\n', '_').replace('\r', '_').replace('\t', '_')


class CustomJSONLog(logging.Formatter):
    elastic_search_logger = None
    f = None

    def __init__(self):
        super().__init__()
        self.f = logging.Formatter('%(asctime)s - %(levelname)s - %(msg)s')
        if "ELASTICSEARCH_MONITOR_HOSTS" in os.environ and os.environ["ELASTICSEARCH_MONITOR_HOSTS"] != "":
            from custom.elasticsearch_shoveler import ElasticSearchLogger
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
        formatted_date = util.iso_time_format(utcnow)
        json_log_object = {"type": "log",
                           "date": formatted_date,
                           "logger": record.name,
                           "thread": record.threadName,
                           "level": record.levelname,
                           "module": record.module,
                           "caller": record.filename,
                           "funcName": record.funcName,
                           "line_no": record.lineno,
                           "message": _sanitize_log_msg(record),
                           "pid": record.process
                           }

        if hasattr(record, 'props'):
            json_log_object.update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object.update(self.get_exc_fields(record))

        if self.elastic_search_logger:
            self.elastic_search_logger.external_logger(body=json_log_object)

        if "JSON_LOG_CONSOLE" in os.environ and os.environ["JSON_LOG_CONSOLE"] == "1":
            return json_serializer(json_log_object)
        else:
            return self.f.format(record)
