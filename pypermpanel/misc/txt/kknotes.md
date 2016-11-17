Stuff too verbose from README.md

## Docker
####docker on normal Ubuntu machine
sudo su
apt-get update
apt-get install apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" |  tee /etc/apt/sources.list.d/docker.list
apt-get update
`apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual` or `apt-get install linux-image-virtual kernel and linux-image-extra-virtual`

#### docker linode

curl -sSL https://get.docker.com/ | sh
http://stackoverflow.com/questions/37227349/unable-to-start-docker-service-in-ubuntu-16-04/37640824#37640824

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



