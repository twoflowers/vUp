FROM debian:latest
MAINTAINER vUp

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install php5-fpm -y

RUN mkdir /data;mkdir /var/www

ADD www.conf /etc/php5/fpm/pool.d/www.conf

RUN service php5-fpm start

EXPOSE 9000

WORKDIR /data

CMD /usr/sbin/php5-fpm --fpm-config /etc/php5/fpm/php-fpm.conf --nodaemonize
