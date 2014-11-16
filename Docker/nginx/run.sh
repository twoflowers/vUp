#!/bin/bash
sed -i  -e "s/%fpm-ip%/${PHP_FPM_IP}/g" /etc/nginx/nginx.conf 
/usr/sbin/nginx -c /etc/nginx/nginx.conf
