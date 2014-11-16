# builtin
import logging
import json
from time import time

# shared
from library import db
from library import exc

# config
from config import shared_config

logger = logging.getLogger(shared_config.api_log_root_name + __name__)


# helpers
def proj_id(project_id):
    return "projects:project:" + project_id


def proj_exists(project_id):
    return db.pipe.exists(name=proj_id(project_id)).execute()[0]


# endpoint gate
def create(name, containers, version):
    project_id = int(time())

    try:
        project = {"id": project_id, "name": name, "version": version, "containers": containers}
        db.pipe.set(name=proj_id(project_id), value=json.dumps(project)).execute()

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise exc.SystemInvalid()

    return {"project_id": project_id, "created": True}


def listing(listing_id=None):
    logger.debug("entered listing({args})".format(args=locals()))

    if listing_id and not proj_exists(listing_id):
        raise exc.UserNotFound("no project with id {i}".format(id=listing_id))

    try:  # pull all projects
        project_names = db.keys("projects:project:*") or []
        logger.debug("returning list of all projects: {p}".format(p=project_names))
        for project in project_names:
            db.pipe.get(name=project["name"])

    except Exception as e:
        logger.error("failed to pull projects because %s" % e, exc_info=True)
        raise exc.SystemInvalid()

    projects = [json.loads(project) for project in db.pipe.execute()]
    projects = projects if not listing_id else [proj for proj in projects]

    if listing_id:  # pull only one project
        projects = [project for project in projects if project["id"] == int(listing_id)]
        logger.debug("project {n} exists, pulling detail".format(n=listing_id))
        if projects:
            return projects
        else:
            raise exc.UserNotFound("no project with id {i}".format(i=listing_id))

    else:  # return list of details
        return projects


def update(listing_id):

    pass