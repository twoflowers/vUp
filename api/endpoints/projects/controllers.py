# built-in
import logging

# config
from api.config import shared_config

# third party
from flask import Blueprint, request

# shared
from library.response import jsonified
from library import errors

# module
import models

projects_blueprint = Blueprint('projects', __name__, url_prefix=shared_config.api_url_prefix + '/projects')
logger = logging.getLogger(shared_config.api_log_root_name + __name__)

@projects_blueprint.route('/', defaults={"project_name": None}, methods=["GET"])
@projects_blueprint.route('/<project_name>', methods=['GET'])
def listing(project_name):
    try:
        return jsonified(data=models.listing(name=project_name))

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
        logger.error("failed to setup variables passed in because %s" % e, exc_info=True)
        raise errors.InvalidUsage()

    # if not isinstance(containers, list) or \
    #         any(not isinstance(container, dict) for container in containers) or \
    #         any(not isinstance(v, (int, unicode, str, long)) for con in containers for k, v in con.iteritems()):
    #     raise errors.InvalidUsage("invalid container format")

    try:
        return jsonified(data=models.create(name=name, containers=containers, version=version))

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise errors.Unhandled()


