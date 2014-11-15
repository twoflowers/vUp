FROM debian:latest
MAINTAINER vUp


RUN apt-get update
RUN apt-get install php5-fpm -y

RUN mkdir /data

ADD www.conf /etc/php5/fpm/pool.d/www.conf

RUN service php5-fpm start

EXPOSE 9000

WORKDIR /data