FROM debian:latest
MAINTAINER vUp


RUN apt-get update
RUN apt-get install nginx -y

ADD vup.conf /etc/nginx/conf.d/vup.conf

RUN service nginx start

EXPOSE 80 81 4001 3001 4001/udp 3001/udp