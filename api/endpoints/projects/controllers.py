# built-in
import logging

# config
from api.config import shared_config

# third party
from flask import Blueprint, request

# shared
from library import db
from library.response import jsonified
from library import errors

# module
import models

projects_blueprint = Blueprint('projects', __name__, url_prefix=shared_config.api_url_prefix + '/projects')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)

@projects_blueprint.route('/', defaults={"project_id": None}, methods=["GET"])
@projects_blueprint.route('/<project_id>', methods=['GET'])
def listing(project_id):
    try:
        keys = db.keys() or []
        return jsonified(data="keys are currently {k}, you wanted to view {p}".format(k=keys, p=project_id))

    except Exception as e:
        logger.error("unhandled error {e}".format(e=e), exc_info=True)
        raise errors.Unhandled()


@projects_blueprint.route("/<project_name>", methods=['PUT'])
def update(project_name):
    try:
        args = request.get_json(force=True)
        new_project_name = args.get('name')
        project_version = args.get('version')
        container_name = project_name + ":containers:"
        container_map = args.get('containers')
        project_map = {"name": "projects:{n}".format(n=new_project_name or project_name), "verson": project_version}
    except Exception:
        raise errors.InvalidUsage()



    # update

@projects_blueprint.route("/", methods=["POST"])
def create():
    try:  # get project fields
        args = request.get_json(force=True)
        name = args['name']
        version = args['version']
        containers = args['containers']

    except Exception as e:
        raise errors.InvalidUsage()

    if not isinstance(containers, list) or any(not isinstance(c, (int, unicode, str, long)) for c in containers):
        raise errors.InvalidUsage("invalid container format")

    try:
        return jsonified(data=models.create_project(name=name, containers=containers, version=version))

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise errors.Unhandled()


