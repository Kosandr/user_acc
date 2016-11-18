FROM ubuntu:16.04
MAINTAINER Konstantin Kowalski <kostelkow@gmail.com>
RUN apt-get install -y software-properties-common && apt-key a
RUN apt-get update && apt-get install -y nginx python3 redis-server
RUN pip3 install flask Flask-Session SQLAlchemy mysqlclient gunicorn libsass sh
RUN apt install -y curl && curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash - && apt-get install -y nodejs

