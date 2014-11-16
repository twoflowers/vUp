# builtin
import logging
import json
from time import time

# shared
from library import db
from library import exc
from library import dockerhelper as docker

# config
from config import shared_config

logger = logging.getLogger(shared_config.api_log_root_name + __name__)


# helpers
def proj_name(name):
    return "projects:project:" + str(name).encode('base64', 'strict')


def proj_exists(name):
    return db.pipe.exists(name=proj_name(name)).execute()[0]


# endpoint gate
def create(name, containers, version):
    if proj_exists(name):
        raise exc.UserInvalidUsage("unable to overwrite existing project")

    try:
        project = {"id": int(time()), "name": name, "version": version, "containers": containers}
        db.pipe.set(name=proj_name(name), value=json.dumps(project)).execute()
        c = docker.get_client(host_url="tcp://docker1:2375")
        docker.create_containers_from_proj(docker_client=c, project_name=name, project_containers=containers)

    except Exception as e:
        logger.error("failed to create new project because %s" % e, exc_info=True)
        # TODO rollback on error, deleting keys possibly created
        raise exc.SystemInvalid()

    return {"project": name, "created": True, "value": project}


def listing(name=None):
    logger.debug("entered listing({args})".format(args=name))
    if name:  # return only that project
        if proj_exists(name=name):
            logger.debug("project {n} exists, pulling detail".format(n=name))
            return json.loads(db.pipe.get(name=proj_name(name=name)).execute())
        else:
            raise exc.UserNotFound("no project named {n}".format(n=name))

    else:  # return list of details
        try:
            project_names = db.keys("projects:project:*") or []
            logger.debug("returning list of all projects: {p}".format(p=project_names))

            for project in project_names:
                db.pipe.get(name=project["name"])

            return [json.loads(project) for project in db.pipe.execute()]
        except Exception as e:
            logger.error("failed to list projects because %s" % e, exc_info=True)
            raise exc.SystemInvalid()
