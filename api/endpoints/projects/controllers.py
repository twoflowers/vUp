# built-in
import logging

# config
from api.config import shared_config

# third party
from flask import Blueprint, request

# shared
from library.response import jsonified
from library import errors, exc

# module
import models

projects_blueprint = Blueprint('projects', __name__, url_prefix=shared_config.api_url_prefix + '/projects')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)

@projects_blueprint.route('/', defaults={"project_id": None}, methods=["GET"])
@projects_blueprint.route('/<project_id>', methods=['GET'])
def listing(project_id):
    try:
        return jsonified(data=models.project_listing(project_id=project_id))

    except exc.UserNotFound as e:
        raise errors.NotFound(e)

    except Exception as e:
        logger.error("unhandled error {e}".format(e=e), exc_info=True)
        raise errors.Unhandled()


@projects_blueprint.route("/<project_id>", methods=['PUT'])
def update(project_id):
    try:
        args = request.get_json(force=True)
        project_name = args.get('name')
        project_version = args.get('version')
        project_containers = args.get('containers')
        project_map = {"name": "projects:{n}".format(n=project_name or project_id), "version": project_version}

    except Exception:
        raise errors.InvalidUsage()

@projects_blueprint.route("/<project_id>", methods=['DELETE'])
def remove(project_id):
    try:
        return jsonified(data=models.project_delete(project_id=project_id))

    except Exception:
        raise errors.InvalidUsage()


@projects_blueprint.route("/", methods=["POST"])
def create():
    try:  # get project fields
        args = request.get_json(force=True)
        name = args['name']
        version = args['version']
        containers = args['containers']

    except Exception as e:
        logger.error("failed to setup variables passed in because %s" % e, exc_info=True)
        raise errors.InvalidUsage()

    try:
        return jsonified(data=models.project_create(name=name, containers=containers, version=version))

    except exc.SystemInvalid as e:
        raise errors.Unhandled(e)
    except exc.UserInvalidUsage as e:
        raise errors.InvalidUsage(e)

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise errors.Unhandled()


