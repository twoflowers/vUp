# builtin
import logging

# config
from config import shared_config

# third party
from flask import jsonify
from werkzeug.exceptions import MethodNotAllowed

# shared
from library import errors

logger = logging.getLogger(shared_config.api_log_root_name + __name__)


def jsonified(data, code=None):
    if isinstance(data, (Exception, errors.Errors, MethodNotAllowed)):
        try:
            status = code or data.status
        except:
            try:
                status = code or data.code
            except:
                status = code or 500
        if isinstance(data, MethodNotAllowed):
            message = data.description
        else:
            message = data.message


        resp = {"data": message, "status": status, "success": False}
    else:
        resp = {"data": data, "status": code or 200, "success": True}

    logger.debug("responding with ({s}){d}".format(d=resp, s=resp['status']))
    return jsonify(resp), resp['status']


def register_error_handlers(flask_app, *errors_handled):
    """ bulk registering errors that are handled in same manner """

    def handler(error):
        logger.debug("sending error %r to jsonified" % error)
        return jsonified(data=error)

    logger.debug("registering error handlers %r" % str(errors_handled))
    for error in errors_handled:
            flask_app.register_error_handler(code_or_exception=error, f=handler)
    logger.debug("finished registering error handlers")
