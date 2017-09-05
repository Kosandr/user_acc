FROM ubuntu:16.04
MAINTAINER Konstantin Kowalski <kostelkow@gmail.com>

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y nginx python3 python3-pip redis-server git
RUN pip3 install Flask

#Mariadb
#password issue: http://dba.stackexchange.com/questions/35866/install-mariadb-without-password-prompt-in-ubuntu
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y software-properties-common && apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8 && add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://mariadb.mirror.anstey.ca/repo/10.1/ubuntu xenial main'; apt update; DEBIAN_FRONTEND=noninteractive apt install -y mariadb-server libmariadbclient-dev

#python/flask/gunicorn/libsass packages
#possibly need python-mariadb and python-mysqldb
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip libssl-dev && pip3 install --upgrade pip; pip3 install flask Flask-Session SQLAlchemy mysqlclient gunicorn libsass sh redis

#node
RUN DEBIAN_FRONTEND=noninteractive apt install -y curl && curl -sL https://deb.nodesource.com/setup_7.x | bash - && DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
RUN npm install --save-dev -g babel-cli babel-reset-latest; npm install -g babel-plugin-transform-react-jsx; npm install --save-dev babel-preset-es2015

