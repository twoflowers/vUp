# Built-in
import logging

# Config
from api.config import shared_config

# 3rd Party
from flask import Blueprint, jsonify

# Shared


status_blueprint = Blueprint('status', __name__, url_prefix=shared_config.api_url_prefix + '/status')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)


@status_blueprint.route('/', methods=['GET'])
def update():
    return jsonify(data=["update is coming, you gave me"])