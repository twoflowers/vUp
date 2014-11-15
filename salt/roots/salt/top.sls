base:
  '*':
#      - iptables
      - misc
  'vup*':
      - nginx
      - uwsgi
      - pip
      - redis
  'vocker*':
      - docker
