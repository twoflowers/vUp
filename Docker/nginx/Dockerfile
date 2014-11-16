FROM debian:latest
MAINTAINER vUp

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install nginx -y
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
ADD run.sh /run.sh

EXPOSE 80 81 4001 3001 4001/udp 3001/udp

CMD /run.sh
