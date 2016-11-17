
### Installation instructions

Requires ubuntu 16.04

- install docker from the official website.
- run `sudo usermod -aG docker $USER` to add your user to docker group


### Main TODO/NOTES/README for new permission system

- [ ] SQLAlchemy user storage and permission system (src/pyperm.py)
- [ ] generic apps on each desktop/site, and can have multiple desktops
- [ ] start using proper markup
- [ ] use exceptions
- [ ] logging
- [ ] some pycloak stuff
- [ ] Travis ci integration
- [ ] use python virtual environments

Naming ideas
- pypermpanel/ppp
- pywebdesk/webdesk


### Docker notes

```bash
abbreviations
   <intContName> = internal container name given by docker
      can also use CONTAINER ID
```
#### Basic usage:

```bash
docker run hello-world
docker run ubuntu /bin/echo 'Hello, world!'
docker run -d -P training/webapp python app.py

docker run [--name='blah'] [-P] [-d] [-t] [-i] <containerImageName> <cmdName>
   options
      -P = publish all exposed ports to random ports
      -d = detach/daemon/run in background
      -t = assigns a pseudo-tty or terminal inside the new container
      -i = start interactive connection (grabs STDIN of the container)
      -p = see ports section
   interactive shell
      docker run -t -i ubuntu /bin/bash
      docker run -it ubuntu /bin/bash
   daemonized Hello World
      cmd="while true; do echo hello world; sleep 1; done"
      docker run -d ubuntu /bin/sh -c "$cmd"
         returns container ID
   ports
      docker run -d -p 3333:5000 training/webapp python app.py
         binds host's port 3333 to container's port 5000
      docker run -d -P training/webapp python app.py
         -P maps any internal container ports to host
      run "docker ps" to see which port that container is using
         0.0.0.0:3333->5000/tcp
            means that host's port 3333 points to container's 5000

help system
   docker --help
   docker attach --help

docker start <intContName>
   restart container that was ran before

docker stop <intContName>
   stops container that was demonized

docker restart <intContName>
   runs stop and start

docker attach <intContName>
   attaches to demonized container

docker rm [-f] <intContName>
   -f flag forces removal

docker top <intContName>
   top for docker
   prints commands running inside specified container

docker inspect [-f <str>] <intContName>
   prints internal JSON
   print container's ip address:
      docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <intContName>
      docker inspect --format='{{json .NetworkSettings.Networks}}' db

docker logs [-f] <intContName>
   show output of that particular container
   -f flag shows logs interactively without exiting

docker ps [-a] [-l]
   default = print currently running containers
      last column is internal name used to refer to container instance
      first column is container id which can be interchanged with the name
   docker ps -a
      also includes containers which are no longer running
   docker ps -l
      -l specifies last container that was started

docker port <intContName> [<optional containerPortNum>]
   get port being by container used without running "docker ps"
   containerPortNum is used to specify internal port
   ex 1: docker port blah 5000
   ex 2: docker port blah

```

#### Images:
```bash

docker images [--digests]
   lists images currently on machine
   includes REPOSITORY, TAG, IMAGE ID, CREATED and SIZE
   TAG:
      tags can be like ubuntu version
      ex: docker run -t -i ubuntu:14.04 /bin/bash
      without specifying tag, runs ubuntu:latest

   digests
      --digests = print SHA256 checksum of images
      can be used in pull/push
         docker pull uname/sinatra@sha256:cbbf2f9a...

docker rmi <imageName/digest>
   remove image
   ex: docker rmi training/sinatra

docker create
   ???

docker push uname/imgName
   push to repository

docker pull <imageName>
   preloads an image, same way as docker run
   ex:
      docker pull centos
      docker run -t -i centos /bin/bash

docker search sinatra
   search DockerHub

docker tag <contId> <uname/imgName:tag>
   docker tag 5db5f7471261 ouruser/sinatra:devel
```

##### Simple way to make images
```bash

docker commit [-m "Commit Msg"] [-a "Author Name"] <IMAGE_ID> <USERNAME/REPONAME:TAG>
   create custom images
      step 1: pull existing image
      step 2: run an interactive container shell for the image
      step 3: do work and exit
      step 4: docker commit -m "Commit message" -a "Author Name" 0b2616b0e5a8 ouruser/sinatra:v2

   run custom image
      docker run -t -i ouruser/sinatra:v2 /bin/bash
```
##### Dockerfile images
```bash
docker build [-t uname/imgname:tag] . = builds new image
   -t specifies user for image

ex:
   mkdir sinatra && cd sinatra && touch Dockerfile
   Dockerfile content:
      # This is a comment
      FROM ubuntu:14.04
      MAINTAINER Kate Smith <ksmith@example.com>
      RUN apt-get update && apt-get install -y ruby ruby-dev
      RUN gem install sinatra
   docker build -t ouruser/sinatra:v2 .
   docker run -t -i ouruser/sinatra:v2 /bin/bash
```

#### Network containers
```
docker network ls
   print network types: none/host/bridge

   bridge = default
      docker run -itd --name=networktest ubuntu

docker network inspect bridge
   find container's IP

docker network disconnect bridge <netowkrName>
   disconnect container from network

docker network create -b <netType> <name> = create new network
   ex:
      docker network create -d bridge my-bridge-network
      docker network inspect my-bridge-network #get IP address
   network types
      bridge = limited to single host running Docker Engine
      overlay network = inculdes multiple hosts

creating custom network and using it:
   docker network create -d bridge my-bridge-network
   docker network inspect my-bridge-network
      get IP address
   docker run -d --network=my-bridge-network --name db training/postgres
   docker inspect --format='{{json .NetworkSettings.Networks}}' db

   docker run -d --name web training/webapp python app.py
   docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web
      get ip address
   docker network connect my-bridge-network web
      connect web app to our network
   docker exec -it db bash
      root@xxx:/# ping web

```


```bash
Data volumes


```
