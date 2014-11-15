# built-in
import logging

# config
from api.config import shared_config

# third party
from flask import Blueprint

# shared
from library import db
from library.response import jsonified

projects_blueprint = Blueprint('projects', __name__, url_prefix=shared_config.api_url_prefix + '/projects')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)


@projects_blueprint.route('/<project_id>', methods=['GET'])
def listing(project_id):
    keys = db.keys()
    return jsonified(data="keys are currently {k}, you wanted to view {p}".format(k=keys, p=project_id))