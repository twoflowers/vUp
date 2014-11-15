docker-repo:
  pkgrepo.managed:
    - humanname: Docker PPA
    - name: deb http://get.docker.io/ubuntu docker main
    - key_url: https://get.docker.io/gpg
docker:
  pkg.latest:
    - name: lxc-docker 
    - require:
      - pkgrepo: docker-repo
  service.running:
    - name: docker.io
    - enable: true
/etc/default/docker.io:
  file.managed:
    - source: salt://docker-config.conf.jinja
    - require:
      - pkg: docker
    - watch_in:
      - service: docker
