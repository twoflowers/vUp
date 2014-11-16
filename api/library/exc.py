# builtin
import logging

# config
from config import shared_config

logger = logging.getLogger(shared_config.api_log_root_name + __name__)


class Errors(Exception):

    _message = "Whoops! You found a spot that's not working properly"
    _log_level = logging.WARN

    def __init__(self, message=None, log_level=None):
        Exception.__init__(self)
        self.message = message
        self.log_level = log_level
        logger.log(level=self.log, msg=self.message)

    @property
    def log(self):
        return self._log_level

    @log.setter
    def log(self, value):
        self._log_level = value or self._log_level

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value or self._message

    def to_dict(self):
        return {"message": self.message}



class SystemError(Errors):
    _message = "Unhandled error"
    _log_level = logging.ERROR

