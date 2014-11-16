import logging
# config
from config import shared_config
from docker import Client
logger = logging.getLogger(shared_config.api_log_root_name + __name__)

"""
Call get_client first, and then pass it to the other functions
"""

def get_client(host_url):
    """ Returns a docker api client """
    c = Client(base_url=host_url)
    # TODO: Test connection
    return c


def create_container(docker_client, image_name, container_name, env=None, links=None, ports=None, volumes=None, volumes_from=None, command=None):
    #  Links can be specified with the links argument. They can either be specified as a dictionary mapping name to alias or as a list of (name, alias) tuples.
    logger.debug("Creating a new container with: %r" % locals())
    container = docker_client.create_container(image=image_name, environment=env, name=container_name, command=command, ports=ports)
    if volumes is not None:
        vol_binding = {}
        for vol in volumes:
            vol_binding[volumes[vol]] = {
                        'bind': vol,
                        'ro': False
                    }
    else:
        vol_binding = None

    if ports is not None:
        try:
            port_binding = {}
            for port in ports:
                port_no = int(port)
                port_binding[port] = ('0.0.0.0', )
        except Exception as e:
            raise RuntimeError("Port must be int: %r" % e)
    else:
        port_binding = None
    response = docker_client.start(container=container.get('Id'), links=links, binds=vol_binding, volumes_from=volumes_from, port_bindings=port_binding)
    # Return the container id
    return container.get('Id')
    

def create_mysql(docker_client, container_name, db_name, db_user, db_pass=None, db_sql=None, ports=None):
    env = {
                "MYSQL_USER": db_user,
                "MYSQL_PASS": db_pass if db_pass is not None else "**Random**",
            }
    return create_container(docker_client=docker_client, image_name="vups/vup_mysql", container_name=container_name, env=env, ports=ports)

def create_nginx(docker_client, container_name, links=None, ports=None, env=None):
    # Links can be specified with the links argument. They can either be specified as a dictionary mapping name to alias or as a list of (name, alias) tuples.
    return create_container(docker_client=docker_client, image_name="vups/vup_nginx", container_name=container_name, env=env, links=links, ports=ports)

def create_storage(docker_client, container_name, storage_url):
    if 'local://' in storage_url:
        # Only local storage is supported right now.   Path has to exist on the docker host machine
        local_path = storage_url.replace('local://', '')
        return create_container(docker_client=docker_client, container_name=container_name, image_name="debian", volumes={'/data': local_path}, command="/bin/bash -c 'while /bin/true; do sleep 300;done'")
    else:
        raise RuntimeError("%s not supported.  Use local://" % storage_url)

def create_apache(docker_client, container_name, volumes_from, links, ports=None):
    return create_container(docker_client=docker_client, container_name=container_name, image_name="vups/vup_apache", volumes_from=volumes_from, links=links, ports=ports)

def create_phpfpm(docker_client, container_name, volumes_from, links, ports=None):
    if volumes_from is None:
        raise RuntimeError("volumes_from can not be None for create_phpfpm")
    return create_container(docker_client=docker_client, image_name="vups/vup_php_fpm", container_name=container_name, volumes_from=[volumes_from], links=links, ports=ports)

def get_ip(docker_client, container_id):
    return docker_client.inspect_container(container=container_id)['NetworkSettings']['IPAddress']

def get_host_port(docker_client, container_id, port_no):
    container = docker_client.inspect_container(container=container_id)
    host_port = container['NetworkSettings']['Ports']['%d/tcp' % port_no][0]['HostPort']
    # TODO: Get this dynamically
    host_ip = "192.168.4.20"
    return "http://%s:%s/" % (host_ip, host_port)

def get_container_info(docker_client, project_name, container_name):
    try:
        prefix = project_name.strip().replace(' ', '_').lower() + "_"
        real_name = "%s%s" % (prefix, container_name.strip().replace(" ", '').lower())
        container = docker_client.inspect_container(container=real_name)
        data = {
                    'IPAddress': container['NetworkSettings']['IPAddress'],
                    'State': container['State']
                }
        if '80/tcp' in container['NetworkSettings']['Ports']:
            data['url'] = get_host_port(docker_client, container['Id'], 80)
        if '3306/tcp' in container['NetworkSettings']['Ports']:
            data['mysql_port'] = get_host_port(docker_client, container['Id'], 3306).replace('http://', '').replace('/', '')
    except Exception as e:
        data = {}
        logger.error("Error trying to get container_info: %r" % e)

    return data


def process_deps_type(containers, type):
    new_containers = []
    for c in containers:
        if c['type'] == type:
            new_containers.append(c)
    return new_containers
        

def process_deps(project_containers):
    """ Takes a list of containers, and returns an ordered list in the order they should be provisioned. """
    new_containers = []
    # Find storage first
    new_containers = new_containers + process_deps_type(project_containers, 'storage')
    new_containers = new_containers + process_deps_type(project_containers, 'mysql')
    new_containers = new_containers + process_deps_type(project_containers, 'php')
    new_containers = new_containers + process_deps_type(project_containers, 'nginx')
    new_containers = new_containers + process_deps_type(project_containers, 'apache')
    return new_containers

def create_containers_from_proj(docker_client, project_name, project_containers):
    prefix = project_name.strip().replace(' ', '_').lower() + "_"
    # TODO: Get a list of existing containers for project
    # TODO: Error handling
    php_app_ip = None
    mysql_env = None
    for container in process_deps(project_containers):
        clean_name = container['name'].strip().replace(' ', '_').lower()
        container_name = "%s%s" % (prefix, clean_name) 
        logger.debug("Checking if we need to create container_name: %s container_type: %s" % (container_name, container['type']))

        if 'link' in container:
            links = []
            for link in container['link']:
                links.append(("%s%s" % (prefix, link.strip().replace(" ", '').lower()), link))
        else:
            links = None

        if 'volumes_from' in container:
            volumes_from = "%s%s" % (prefix, container['volumes_from'].strip().replace(" ", '').lower())
        else:
            volumes_from = None

        if 'env' in container:
            env = container['env']
        else:
            env = {} 

        if php_app_ip is not None:
            env['PHP_FPM_IP'] = php_app_ip
        if mysql_env is not None:
            env.update(mysql_env)

        ports = None if 'ports' not in container else container['ports']

        if container['type'] == "storage":
            result = create_storage(docker_client=docker_client, container_name=container_name, storage_url=container['data_source'])
        elif container['type'] == "nginx":
            result = create_nginx(docker_client=docker_client, container_name=container_name, links=links, ports=ports, env=env)
        elif container['type'] == "apache":
            result = create_apache(docker_client=docker_client, container_name=container_name, links=links, volumes_from=volumes_from, ports=ports)
        elif container['type'] == "mysql":
            result = create_mysql(docker_client=docker_client, container_name=container_name, db_name=container['mysql_name'], db_user=container['mysql_user'], db_pass=container['mysql_pass'], db_sql=container['mysql_sql'], ports=ports)
            mysql_env = {
                        'mysql_user': container['mysql_user'],
                        'mysql_pass': container['mysql_pass'],
                        'mysql_host': get_ip(docker_client, result),
                        'mysql_name': container['mysql_name']
                    }
        elif container['type'] == "php":
            result = create_phpfpm(docker_client=docker_client, container_name=container_name, volumes_from=volumes_from, links=links)
            php_app_ip = get_ip(docker_client, result)

    return True

def delete_all_containers_from_proj(docker_client, project_name):
    """ Looks for any vms that begin with the prefix of the project name.   TODO:  Do something else. """
    containers = docker_client.containers(all=True)
    prefix = project_name.strip().replace(' ', '_').lower() + "_" 
    for container in containers:
        for container_name in container['Names']:
            if prefix in container_name:
                try:
                    logger.info("deleting container with name: {n}, container: {c}".format(n=container_name, c=container))
                    docker_client.remove_container(container=container['Id'], force=True, v=True)
                except:
                    continue # FIND OUT WHAT TO DO
