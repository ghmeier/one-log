import logging

log = logging.getLogger(__name__)


class OneLog(object):
    START = 'START'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

    @staticmethod
    def info(log_data, **kwargs):
        kwargs = OneLog._format_kwargs(log_data, kwargs)

        log.info(kwargs)

    @staticmethod
    def error(log_data, **kwargs):
        kwargs = OneLog._format_kwargs(log_data, kwargs)

        log.error(kwargs)

    @staticmethod
    def exception(log_data, **kwargs):
        kwargs = OneLog._format_kwargs(log_data, kwargs)

        log.exception(kwargs)

    @staticmethod
    def _format_kwargs(log_data, kwargs):
        kwargs.update({
            'path': log_data.path,
            'state': log_data.state,
            'method': log_data.method,
            'data': log_data.data
        })
        return kwargs

    @staticmethod
    def fail(log_data, data={}):
        log_data.state = OneLog.FAILURE
        return OneLog.update(log_data, data=data)

    @staticmethod
    def succeed(log_data, data={}):
        log_data.state = OneLog.SUCCESS
        return OneLog.update(log_data, data=data)

    @staticmethod
    def update(log_data, data={}):
        log_data.data.update(data)
        return log_data

    @staticmethod
    def get_log_data(path, method, data={}):
        log_data = LogData(path=path, method=method,
                           state=OneLog.START, data=data)
        OneLog.info(log_data)
        return log_data


class LogData(object):

    def __init__(self, path, method, state, data):
        self.path = path
        self.method = method
        self.state = state
        log.info(data)
        self.data = data
