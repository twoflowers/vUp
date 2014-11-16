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
