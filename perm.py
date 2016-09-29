import sqlite3, atomicid, os.path
from flask import Flask, request, send_from_directory

app = Flask(__name__)

DB_PATH = '/tmp/permtest.db'

#can make more generic, and each permission is a Tag
class UserPermissions(Db):
   def __init__(self, dbpath):
      super(UserPermissions, self).__init__(dbpath)
      self.init_tables()

   def add_user(uname):
      pass
   def rm_user(uname):
      pass

   def add_group(groupname):
      pass
   def rm_group(groupname):
      pass

   def add_user_to_group(groupname):
      pass
   def rm_user_from_group(groupname):
      pass

   #this specific itemname can be accessed by this groups
   def add_granual_item(itemname, group_access_list):
      pass

   def check_user_check_granual_resource(itemname, uname):
      pass

   #possibly decorator
   def check_group(group_access):
      pass

   #same as above
   def requires_group(groups):
      pass

   #decorator for each resource, can give it name and it will be managed by granual_item
   def resource_perm(resourcename):
      pass

n = 0
class FormDb:
   def __init__(self):
      need_init = False
      if not os.path.exists(DB_PATH):
         need_init = True

      self.conn = sqlite3.connect(DB_PATH)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

   def init_db(self):
      self.c.execute('''CREATE TABLE contact_form
                        (first_name text)''')
      self.conn.commit()

   def add_contact(self, first):
      self.c.execute('INSERT INTO contact_form VALUES (?)', (first,))
      self.conn.commit()

db = FormDb()
import lock
n = 0
@app.route('/', methods=['POST'])
def on_req():
   global n
   form_db = FormDb()
   f = request.form['name']
   print(f)
   n = n + 1
   lock.get_id(n)
   db.add_contact(f)
   return 'ok'


#l =
def test_objid():
   for i in urange(0, 1000):



