# built-in
import logging
from time import time

# 3rd party library
from flask import Flask

# module library

# config
from config import shared_config

# library library

# blueprints
from status.controllers import status_blueprint


class AppVars(object):
        pass


# Define the WSGI application object, cloudstack application object
app = Flask(__name__)
app.config.from_object('config.app')
app.url_map.strict_slashes = False


# Register blueprint(s)
app.register_blueprint(status_blueprint)


#HTTP Error Handling

logger = logging.getLogger(shared_config.api_log_root_name + __name__)

# Before App Request Functions
@app.before_first_request
def setup_app():
    logger.debug("starting up vUp version {v} started {s}".format(v=1, s=time()))


@app.before_request
def setup_request():
    logger.debug("request time:%s" % time())


@app.after_request
def process_response(response):
    logger.debug("response status code: %s" % response.status_code)

    return response
