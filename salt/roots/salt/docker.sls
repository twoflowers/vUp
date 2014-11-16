docker-repo:
  pkgrepo.managed:
    - humanname: Docker PPA
    - name: deb http://get.docker.io/ubuntu docker main
    - key_url: https://get.docker.io/gpg
docker:
  pkg.installed:
    - name: lxc-docker 
    - require:
      - pkgrepo: docker-repo
  service.running:
    - name: docker
    - enable: true
/etc/default/docker:
  file.managed:
    - source: salt://docker-config.conf.jinja
    - require:
      - pkg: docker
    - watch_in:
      - service: docker
sleep 10; docker pull debian:
  cmd.run:
    - require:
      - service: docker
check mysql:
    cmd.run:
        - name: docker build -t vups/vup_mysql .
        - cwd: /home/vagrant/docker/mysql/
check nginx:
    cmd.run:
        - name: docker build -t vups/vup_nginx .
        - cwd: /home/vagrant/docker/nginx/
check apache:
    cmd.run:
        - name: docker build -t vups/vup_apache .
        - cwd: /home/vagrant/docker/apache/
check php-fpm:
    cmd.run:
        - name: docker build -t vups/vup_php_fpm .
        - cwd: /home/vagrant/docker/php-fpm/
