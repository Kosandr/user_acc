
docker notes are in misc/txt/kknotes.md

single_image_ex
   single image with all the applications together. made as an example

nmpfrsa = Nginx/Mariadb/Python/Flask/React/Sass/sqlAlchemy
   actual docker infrastructure for this project

##nmpfrsa

- Overview
   - separated into 5 volumes and at least 5 containers
      - volumes: database, assets, backend code (py/js/sass source code), and assets
      - containers: main backend server, db, watchers, development
   - sites and apps
      - this project is generic framework, so business logic separated into separate apps
      - sites enable users to run multiple website projects on same server


- volumes
   - database = has MariaDB data
   - assets = images, big binary files, external javascript libraries, etc
      - probably going to be big in size
   - backend = python code used by Main Server container
   - each app can maybe have it's own code volume (see TODO)
- containers
   - main backend server = central access point for the site, puts everything together
      - run nginx server, gunicorn
      - has ro (read-only) access to backend code volume
   - database = runs MariaDB
      - has rw access to db volume
   - watchers = compiles jsx and sass files, re-starts server when needed
      - has rw access to backend code volume
   - development = used for development/debugging
      - rw access to backend code volume
      - all the development happens here
      - has sshfs, vim, tmux

- apps
   - apps can be stuff like shopping cart, login page, etc.
   - some come with the project (login page, desktop, user permissions)
   - additional apps should be installable with package manager

- sites
   - good for hosting websites with different purposes and domain names on same machine


TODO:
   - each app can have it's own volume (or not)
      - 1 for code, and possibly second one separate volume for private db
      - for apps maybe don't need a volume and do git clone when creating image or something



