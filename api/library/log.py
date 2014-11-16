# builtin
import logging
from flask import g

# shared
from config import shared_config


def factory():
    class LogFilter(logging.Filter):
        def filter(self, record):
            try:
                record.client_ip = g.user.ip
            except:
                record.client_ip = None
            try:
                record.session_id = g.trans_id
            except:
                record.session_id = None
            return True
    return LogFilter


def setup():
    LogFilter = factory()
    formatter = logging.Formatter(shared_config.api_log_format)
    logger = logging.getLogger(shared_config.api_log_root_name[:-1])  # root doesn't need trailing '.'
    logger.setLevel(logging.DEBUG)

    # debug log
    log_handler_debug = logging.FileHandler(shared_config.api_log_debug)
    log_handler_debug.setLevel(logging.DEBUG)
    log_handler_debug.setFormatter(formatter)
    log_handler_debug.addFilter(LogFilter())

    # handlers
    logger.addHandler(log_handler_debug)

    return logger