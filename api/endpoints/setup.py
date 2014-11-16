# built-in
from time import time

# third party library
from flask import Flask

# module library

# config

# library library
from library import response
from library import errors
from library import log

# blueprints
from status.controllers import status_blueprint
from projects.controllers import projects_blueprint

# define flask app
app = Flask(__name__)
app.config.from_object('config.app')
app.url_map.strict_slashes = False


# register blueprint(s)
app.register_blueprint(status_blueprint)
app.register_blueprint(projects_blueprint)


# http error handling
response.register_error_handlers(app, 400, 404, 405, 500, errors.NotFound, errors.Unhandled, errors.InvalidUsage)
logger = log.setup()


# before app request functions
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
