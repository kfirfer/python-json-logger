# This example shows how the logger can be set up to use a custom JSON format.
import logging
import json
import traceback
from datetime import datetime


def extra(**kw):
    """Add the required nested props layer"""
    return {'extra': {'props': kw}}


class CustomPlainLog(logging.Formatter):
    """
    Customized logger
    """
    python_log_prefix = 'python.'

    def get_exc_fields(self, record):
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {f'{self.python_log_prefix}exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record):

        json_log_object = {"@timestamp": datetime.utcnow().isoformat(), "level": record.levelname,
                           "message": record.getMessage(), "caller": record.filename + '::' + record.funcName, 'data': {
                f'{self.python_log_prefix}logger_name': record.name,
                f'{self.python_log_prefix}module': record.module,
                f'{self.python_log_prefix}funcName': record.funcName,
                f'{self.python_log_prefix}filename': record.filename,
                f'{self.python_log_prefix}lineno': record.lineno,
                f'{self.python_log_prefix}thread': f'{record.threadName}[{record.thread}]',
                f'{self.python_log_prefix}pid': record.process
            }}
        if hasattr(record, 'props'):
            json_log_object['data'].update(record.props)

        if record.exc_info or record.exc_text:
            json_log_object['data'].update(self.get_exc_fields(record))

        return json.dumps(json_log_object)
