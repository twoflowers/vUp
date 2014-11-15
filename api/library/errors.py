class Errors(Exception):
    _message = "Whoops! You found a spot that's not working properly"
    _status_code = 400

    def __init__(self, message=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status = status_code
        self.payload = payload

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
    _message = "The thing that you though you were looking for is not found in the place you thought it was..."
    _status_code = 404
