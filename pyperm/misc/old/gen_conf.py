#!/usr/bin/python3

import json

CONF_FILE_PATH='conf.json'

APP_ROOT='/dbtnext/'
DOMAIN = 'https://familyape.com/dbtnext'
STATIC_NGINX = DOMAIN + 'static-nginx'

ACCOUNT_DB_PATH = '/sec/db/dbtnext/accounts.db'

SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

SSL_CERT_PATH = '/etc/letsencrypt/live/familyape.com'
SSL_CERT_PRIV = 'privkey.pem'
SSL_CERT_PUB = 'fullchain.pem'

def write_config():
   conf = {}
   conf['APP_ROOT'] = APP_ROOT
   conf['DOMAIN'] = DOMAIN
   conf['STATIC_NGINX'] = STATIC_NGINX
   conf['ACCOUNT_DB_PATH'] = ACCOUNT_DB_PATH
   conf['SECRET_KEY'] = SECRET_KEY
   conf['SSL_CERT_PATH'] = SSL_CERT_PATH
   conf['SSL_CERT_PRIV'] = SSL_CERT_PRIV
   conf['SSL_CERT_PUB'] = SSL_CERT_PUB
   with open(CONF_FILE_PATH, 'w') as f:
      f.write(json.dumps(conf))

write_config()
exit()

