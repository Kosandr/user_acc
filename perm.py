import sqlite3, atomicid, os.path
from flask import Flask, request, send_from_directory
import dbhelpers

app = Flask(__name__)

DB_PATH = '/tmp/permtest.db'

#can make more generic, and each permission is a Tag
class UserPermissions(dbhelpers.Db):

   def _init_perm_table(self):
      self.c.execute('''CREATE TABLE perm_groups (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_users (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_group_members (objid integer, group_id integer, user_id integer)''')

      self.c.execute('''CREATE TABLE perm_resources (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_resource_allowed_groups (resource_id integer, group_id integer)''')

   def __init__(self, dbpath):
      super(UserPermissions, self).__init__(dbpath)
      self.tables_need_exist['perm'] = self._init_perm_table
      self.init_tables()


   def _get_gid(self, gname):
      self.c.execute('SELECT objid FROM perm_groups WHERE name = ?', (gname, ))
      gid = self.c.fetchone()
      if gid is None:
         return None
      return gid[0]

   def _get_uid(self, uname):
      self.c.execute('SELECT objid FROM perm_users WHERE name = ?', (uname, ))
      uid = self.c.fetchone()
      if uid is None:
         return None
      return uid[0]

   #1 = success, 2 = failure already exists, 3 = failure bad name (short)
   def add_user(self, uname):
      if len(uname) < 5:
         return 3
      if self._get_uid(uname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_users VALUES (?, ?)', (self.get_id(), uname))
      self.conn.commit()
      return 1

   #1 = sucess, 2 = user never existed, (possibly 3 = user is admin)
   def rm_user(self, uname):
      self.c.execute('SELECT objid FROM perm_users WHERE name = ?', (uname, ))
      uId = self.c.fetchone()

      uId = self._get_uid(uname)
      if uId is None:
         return 2
      self.c.execute('DELETE FROM perm_users WHERE objid = ?', (uId, ))
      self.conn.commit()
      return 1

   #1 = success, 2 = already exists
   def add_group(self, groupname):
      if self._get_gid(groupname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_groups VALUES (?, ?)', (self.get_id(), groupname))
      self.conn.commit()
      return 1

   #1 = success, 2 = failure doesn't exist
   def rm_group(groupname):
      groupId = self._get_gid(groupname)
      if groupId is None:
         return 2
      self.c.execute('DELETE FROM perm_groups WHERE objid = ?', (groupId, ))
      self.conn.commit()
      return 1

   #1 = success
   #2 = group doesn't exist
   #3 = user doesn't exist
   #4 = user already in group
   def add_user_to_group(groupname, uname):
      gId = self._get_gid(groupname)
      if gId is None:
         return 2

      uId = self._get_uid(uname)
      if uId is None:
         return 3

      self.c.execute('SELECT objid FROM perm_group_members WHERE group_id = ? AND user_id = ?', (gId, uId))
      objId = self.c.fetchone()
      if objId is not None:
         return 4

      self.c.execute('INSERT INTO perm_group_members VALUES (?, ?, ?)', (self.get_id(), gId, uId))
      self.conn.commit()
      return 1

   #1 = success
   #2 = group doesn't exist
   #3 = user doesn't exist
   #4 = user not in group
   def rm_user_from_group(groupname, uname):
      gId = self._get_gid(groupname)
      if gId is None:
         return 2

      uId = self._get_uid(uname)
      if uId is None:
         return 3

      self.c.execute('SELECT objid FROM perm_group_members WHERE group_id = ? AND user_id = ?', (gId, uId))
      objId = self.c.fetchone()
      if objId is None:
         return 4
      objId = objId[0]

      self.c.execute('DELETE FROM perm_group_members WHERE objid = ?',  (objId, ))
      return 1


   def _get_rid(self, res_name):
      self.c.execute('SELECT objid FROM perm_resources WHERE name = ?', (res_name, ))
      rid = self.c.fetchone()
      if rid is None:
         return None
      return rid[0]

   ###newer new

   #1 = success
   #2 = resource already exists
   #3 = one of groups doesn't exist
   #declare resource, and its access rights
   def perm_add_resource(self, res_name, groups=[]):
      rid = self._get_rid(res_name)
      if rid is not None:
         return 2
      rid = self.get_id()
      self.c.execute('INSERT INTO perm_resources VALUES (?, ?)', (rid, res_name))

      for group in groups:
         ret = self.perm_resource_add_group(group)
         if ret != 1:
            return ret
      return 1

   #1 = success
   #def perm_modify_resource_rights(res_name):
   def perm_resource_add_group(res_name, group_name):
      rid = self._get_rid(rid,
      pass
   def perm_resource_rm_group(res_name, group_name):
      pass

   #decorator. Passes arg "allowed"
   def perm_resource_name(name):
      pass

   #TODO: optional
   #decorator
   def requires_group(name):
      pass


   ###older ew

   #resource access rights
   def perm_add_resource(res_name, groups, users):
      pass

   #def perm_modify_resource_rights(res_name):
   def perm_resource_add_group(name, group_name):
      pass
   def perm_resource_rm_group(name, group_name):
      pass
   def perm_resource_add_user(name, uname):
      pass
   def perm_resource_rm_user(name, uname):
      pass

   #decorator. Passes arg "allowed"
   def perm_resource_name(name):
      pass

   #TODO: optional
   #decorator
   def requires_group(name):
      pass

   ###old

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


'''
add_group('viewer')
add_group('modifier')
add_group('privaleged_viewer')
add_group('privaleged_modifier')
add_group('admin')

@requires_group('admin')
def approve_user(uname):
   pass

@requires_group('admin')
def add_user_to_group(uname, grp):
   pass

def get_report(reportname):
   pass

def view_report():
   pass
'''

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



