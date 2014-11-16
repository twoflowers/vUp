FROM debian:latest
MAINTAINER vUp

RUN apt-get update
RUN apt-get install apache2 -y

# Add Apache configuration
# ADD vup.conf /etc/apache2/conf.d/vup.conf

# Update the default apache site with the config we created.
ADD vup.conf /etc/apache2/sites-enabled/000-default.conf

# Manually set up the apache environment variables
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

# Copy site into place.
ADD www /var/www

# RUN service apache2 start

EXPOSE 80 81 4001 3001 4001/udp 3001/udp

# By default, simply start apache.
CMD /usr/sbin/apache2ctl -D FOREGROUND
