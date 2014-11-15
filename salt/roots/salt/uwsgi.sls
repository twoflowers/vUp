uwsgi:
  pkg.installed:
    - name: uwsgi
  service.running:
    - enable: True
uwsgi-plugin-python:
  pkg.installed:
    - require:
      - pkg: uwsgi
/etc/uwsgi/apps-enabled/vup:
  file.managed:
    - source: salt://uwsgi.ini
    - require:
      - pkg: uwsgi
    - watch_in:
      - service: uwsgi
