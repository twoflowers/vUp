redis:
  pkg.installed:
    - name: redis-server
  service.running:
    - name: redis-server
    - require:
      - pkg: redis
redis-cli:
  pkg.installed:
    - name: redis-tools
