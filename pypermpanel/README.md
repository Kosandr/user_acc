
### Installation instructions

Requires ubuntu 16.04

- install docker from the official website.
- run `sudo usermod -aG docker $USER` to add your user to docker group

##### building docker image
docker build -t rastapasta42/py-flask-react-sass-sqlalchemy .
docker push rastapasta42/py-flask-react-sass-sqlalchemy


##### running server & ssh into image
docker run -it rastapasta42/py-flask-react-sass-sqlalchemy


### Main TODO/NOTES/README for new permission system
- [ ] Docker
   - [ ] Separate docker containers into following:
      - [ ] MariaDB database
      - [ ] backend flask python logic
      - [ ] watcher scripts for react .jsx & Sass compiler
      - [ ] separate container for editor/debugger and tmux
      - [ ] http frontend with nginx
   - [ ] separate storage units
      - [ ] mariadb write/read for front-end and debugger
      - [ ] static data and generated static files
      - [ ] flask python source code
         - [ ] read-only for flask logic container
         - [ ] but watcher and debugger can read/write
      - [ ] logs
      - [ ] credential access
         - [ ] isolate each credential file
         - [ ] use single file instead of volumes
- [ ] various branches for development and production use
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



