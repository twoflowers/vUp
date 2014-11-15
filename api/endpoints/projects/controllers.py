# Built-in
import logging

# Config
from api.config import shared_config

# 3rd Party
from flask import Blueprint, jsonify

# Shared


projects_blueprint = Blueprint('projects', __name__, url_prefix=shared_config.api_url_prefix + '/projects')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)


@projects_blueprint.route('/', methods=['GET'])
def update():
    return jsonify(data=["update is coming, you gave me"])