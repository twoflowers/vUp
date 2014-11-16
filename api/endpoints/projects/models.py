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
    return "projects:project:{id}".format(id=project_id)


def proj_exists(project_id):
    proj_key = proj_id(project_id)
    logger.debug("checking if proj key {p}".format(p=proj_key))
    return db.pipe.exists(name=proj_key).execute()[0]


# endpoint gate
def project_create(name, containers, version):
    project_id = str(int(time()))

    try:
        project = {"id": project_id, "name": name, "version": version, "containers": containers}
        db.pipe.set(name=proj_id(project_id), value=json.dumps(project)).execute()

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise exc.SystemInvalid()

    return {"project_id": project_id, "created": True}


def project_listing(project_id=None):
    logger.debug("entered listing({args})".format(args=locals()))

    if project_id and not proj_exists(project_id):
        raise exc.UserNotFound("no project with id {i}".format(id=project_id))

    try:  # pull all projects
        project_names = db.keys("projects:project:*") or []
        logger.debug("returning list of all projects: {p}".format(p=project_names))
        for project in project_names:
            db.pipe.get(name=project["name"])

    except Exception as e:
        logger.error("failed to pull projects because %s" % e, exc_info=True)
        raise exc.SystemInvalid()

    projects = [json.loads(project) for project in db.pipe.execute()]
    projects = projects if not project_id else [proj for proj in projects]

    if project_id:  # pull only one project
        projects = [project for project in projects if project["id"] == int(project_id)]
        logger.debug("project {n} exists, pulling detail".format(n=project_id))
        if projects:
            return projects
        else:
            raise exc.UserNotFound("no project with id {i}".format(i=project_id))

    else:  # return list of details
        return projects


def update(listing_id):

    pass