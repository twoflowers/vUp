nginx:
  pkg.installed:
    - name: nginx
  service.running:
    - name: nginx
    - enable: true
    - require:
      - pkg: nginx
/etc/nginx/sites-enabled/default:
  file.absent:
    - require:
      - pkg: nginx
/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx.conf.jinja
    - require:
      - file: /etc/nginx/sites-enabled/default
    - watch_in:
      - service: nginx
/etc/nginx/sites-enabled/vup.dev.conf:
  file.managed:
    - source: salt://nginx.vhost.conf.jinja
    - watch_in:
      - service: nginx
