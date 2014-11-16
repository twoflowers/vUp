# builtin
import logging

# config
from config import shared_config

logger = logging.getLogger(shared_config.api_log_root_name + __name__)

class Errors(Exception):

    _message = "Whoops! You found a spot that's not working properly"
    _status_code = 400
    _log_level = logging.WARN

    def __init__(self, message=None, status_code=None, payload=None, log_level=None):
        Exception.__init__(self)
        self.message = message
        self.status = status_code
        self.payload = payload
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

    @property
    def status(self):
        return self._status_code

    @status.setter
    def status(self, value):
        self._status_code = value or self._status_code

    def to_dict(self):
        return {"message": self.message, "status_code": self.status, "payload": self.payload}


class NotFound(Errors):
    _message = "The thing that you thought you were looking for is not found in the place you'd wish it was..."
    _status_code = 404


class Unhandled(Errors):
    _message = "Oops! You found a mistake!"
    _status_code = 500
    _log_level = logging.ERROR
