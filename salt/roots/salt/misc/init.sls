#setenforce 0 || exit 0:
#  cmd:
#    - run
#service iptables stop:
#  cmd:
#    - run
puppet:
  service.dead:
    - enable: false
chef-client:
  service.dead:
    - enable: false
salt-minion:
  service.dead:
    - enable: false
docker1:
  host.present:
    - ip: 192.168.4.20
