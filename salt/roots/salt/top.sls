base:
  '*':
#      - iptables
      - misc
  'vup*':
      - nginx
      - uwsgi
      - pip
      - redis
  'docker*':
      - docker
