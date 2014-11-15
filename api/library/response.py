# builtin
import logging


# config
from config import shared_config

# third party
from flask import jsonify


logger = logging.getLogger(shared_config.api_log_root_name + __name__)


def jsonified(data, code=None):
    resp = {"data": data.message, "status": code or 500, "success": False} if isinstance(data, Exception)\
        else {"data": data, "status": code or 200, "success": True}
    logger.debug("responding with (s){d}".format(d=resp, c=resp['status']))
    return jsonify(data=resp, code=resp['status'])


def register_error_handlers(flask_app, *errors_handled):
    """ bulk registering errors that are handled in same manner """

    def handler(error):
        logger.debug("handler sending error %r to jsonified" % error)
        return jsonified(data=error)

    logger.debug("registering error handlers %r" % str(errors_handled))
    for error in errors_handled:
            flask_app.register_error_handler(code_or_exception=error, f=handler)
    logger.debug("finished registering error handlers")
