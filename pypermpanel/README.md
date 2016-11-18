
### Installation instructions

Requires ubuntu 16.04

- install docker from the official website.
- run `sudo usermod -aG docker $USER` to add your user to docker group

##### building docker image
docker build -t rastapasta42/py-flask-react-sass-sqlalchemy .
docker push rastapasta42/py-flask-react-sass-sqlalchemy

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


