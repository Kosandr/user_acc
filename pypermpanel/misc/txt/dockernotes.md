Stuff too verbose from README.md

##Installation
####docker on normal Ubuntu machine
```bash
sudo su
apt-get update
apt-get install apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" |  tee /etc/apt/sources.list.d/docker.list
apt-get update```

`apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual` or `apt-get install linux-image-virtual kernel and linux-image-extra-virtual`

#### docker linode

`curl -sSL https://get.docker.com/ | sh`

http://stackoverflow.com/questions/37227349/unable-to-start-docker-service-in-ubuntu-16-04/37640824#37640824

good tutorials
   haven't done yet:
      https://docs.docker.com/engine/userguide/intro/
   !!! Learn by example (tutorial from which notes are based)
      https://docs.docker.com/engine/tutorials/dockerizing/

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
docker images
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

#### Data volumes:
```bash

docker run -v [<HostVolumeLocation>:]<ContainerVolumeMountPoint>[:ro]
   creates new volume
   flag ex
      -v /webapp = anonymous
      -v volumeName:/blah = mounts to named volume stored by docker
      -v volumeName/webapp:ro = read only docker volume
      -v /host/path:/webapp = mount to host path (needs to be absolute)
      -v run --rm -it -v ~/.bash_history:/root/.bash_history ubuntu /bin/bash
         mount single file
   ex:
      docker run -d -P --name web -v /webapp ubuntu /bin/echo hello
   host directory mounting
      -v /host/path:/webapp = cannot mount host form Dockerfile
   inspecting volumes
      docker inspect web = prints json: "Mounts": [ ... ]
   - stores actual data for anonymous volumes at /var/lib/docker/volumes

docker volume ls [-f dangling=true]
   list volumes
   flags
      -f dangling=true - list dangling containers

removing containers
   docker run --rm -v /foo -v awesome:/bar busybox top
      delete anonmymouse volume foo but not awesome
   docker rm -v <contName>
      remove container and volumes. resolves dangling containers
   docker rm <volumeName>
      not recommended, dangling containers
   docker volume ls -f dangling=true
      see all dangling containers
   docker volume rm <volumeName>

backup, resture, migrate data
   docker run --rm --volumes-from dbstore -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /dbdata
      back data from dbstore into (local folder) backup/backup.tar

   restore backup
      docker run -v /dbdata --name dbstore2 ubuntu /bin/bash
      docker run --rm --volumes-from dbstore2 -v $(pwd):/backup ubuntu bash -c "cd /dbdata && tar xvf /backup/backup.tar --strip 1"

creating and mounting a data volume container
   docker create -v /dbdata --name dbstore training/postgres /bin/true
      doesn't run an app, but re-uses training/postgres for layers
   docker run -d --volumes-from dbstore --name db1 training/postgres
      uses --volumes-from to mount the /dbdata
   docker run -d --volumes-from dbstore --name db2 training/postgres
      same thing
   docker run -d --name db3 --volumes-from db1 training/postgres
      same thing but mounts on top of db1 instead of dbstore
   "docker rm -v db3" or "docker  volume rm volumeName"
      remove all containers. needs to be called with last created

docker volume = TODO research shared-storage volumes as data volumes
   docker volume create -d focker -o size=20GB my-named-volume
      create shared-storage volume
   docker run -d -P \
         --volume-driver=focker \
         -v my-named-volume:/webapp \
         --name web training/webapp python app.py
   iSCSI, NFS, or FC
   https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-shared-storage-volume-as-a-data-volume

Dockerfile
   use VOLUME instruction

```


#### docker links

- installation
   https://docs.docker.com/engine/installation/linux/ubuntulinux/
- linode issue
   https://github.com/docker/docker/issues/22371
- good links
   - Dockerfile docs/guidelines/good practices
      - https://docs.docker.com/engine/reference/builder/
      - https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/
   -  Building your own image
      - https://docs.docker.com/engine/getstarted/step_four/
   - Docker Hub
      - https://hub.docker.com/
      - Official Dockerhub repositories
         - https://docs.docker.com/docker-hub/official_repos/
         - https://hub.docker.com/explore/
      - automated builds
         - https://docs.docker.com/engine/tutorials/dockerrepos/#automated-builds
   - Visualizing images
      - https://imagelayers.io/
      - https://github.com/justone/dockviz
   - Ubuntu docker installation
      - https://docs.docker.com/engine/installation/linux/ubuntulinux/
   - Docker docs good
      - https://docs.docker.com/
   - Get started with docker
      - https://docs.docker.com/engine/getstarted/
   - Installing on Linux
      - https://docs.docker.com/engine/installation/linux/ubuntulinux/
- other misc links
   - storage engines
      - [ ] https://docs.docker.com/engine/userguide/storagedriver/selectadriver/
      - [ ] https://docs.docker.com/engine/userguide/storagedriver/imagesandcontainers/
      - [ ] https://docs.docker.com/engine/userguide/storagedriver/selectadriver/
   - linode-related
      - [ ] https://www.linode.com/docs/applications/containers/how-to-install-docker-and-deploy-a-lamp-stack
      - [ ] https://www.linode.com/docs/applications/containers/how-to-install-docker-and-deploy-a-lamp-stack
      - [ ] https://www.linode.com/docs/tools-reference/custom-kernels-distros/run-a-distribution-supplied-kernel-with-kvm
   - tabs
      - https://docs.docker.com/machine/
      - https://docs.docker.com/engine/installation/linux/ubuntulinux/
      - https://docs.docker.com/
      - https://docs.docker.com/engine/getstarted/
      - https://docs.docker.com/engine/tutorials/dockerizing/
      - https://docs.docker.com/docker-hub/official_repos/
      - https://hub.docker.com/explore/
      - https://docs.docker.com/engine/tutorials/dockerizing/
      - https://docs.docker.com/engine/reference/builder/
      - https://docs.docker.com/engine/getstarted/step_four/

