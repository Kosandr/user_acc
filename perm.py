import sqlite3, atomicid, os.path
from flask import Flask, request, send_from_directory
import dbhelpers

app = Flask(__name__)
DB_PATH = '/tmp/permtest.db'

######################
#perms are asrw, a being (a)dministrator privelages (can give out read/write), and s is (s)uper admin which can give out admin and superadmin
#perms = Perm([Perm.ADMIN, Perm.SUPER, Perm.READ, Perm.WRITE])

#x = Perm([Perm.ADMIN, Perm.SUPER])
#x = Perm(0 | Perm.ADMIN | Perm.SUPER)
#x = Perm('asrw')
#x = Perm(Perm.ADMIN)

#x = Perm(Perm.ADMIN | Perm.WRITE)
#y = Perm(x)
#z = Perm(y.val | Perm.WRITE) #new perm z with same permissions as y, plus write

#x.get_status() == 0
#x.has_read(), x.has_write(), x.has_admin(), x.has_super_admin()

######################

class Perm(object):
   ADMIN = (1 << 0)
   SUPER = (1 << 1)
   READ = (1 << 2)
   WRITE = (1 << 3)
   _ALL_ARR = [ADMIN, SUPER, READ, WRITE]

   def save_arr(self, arr):
      self.val = 0
      for x in arr:
         if x not in Perm._ALL_ARR:
            return 1
         self.val = self.val | x

      if not self.check_num_valid(self.val):
         return 3
      return 0

   def save_str(self, string):
      self.val = 0

      good = list('asrw')
      for c in string:
         if c not in good:
            return 1
         if c == 'a':
            self.val = self.val | Perm.ADMIN
         elif c == 's':
            self.val |= Perm.SUPER
         elif c == 'r':
            self.val |= Perm.READ
         elif c == 'w':
            self.val |= Perm.WRITE

      if not self.check_num_valid(self.val):
         return 3
      return 0

   # check_num_valid: checks raw value of self.val
   # self.val is underlying format for storage of permission
   # valid = True, invalid = False
   def check_num_valid(self, n):
      if n is None:
         return False
      all_perms = 0
      for x in Perm._ALL_ARR:
         all_perms |= x
      if (n | all_perms) != all_perms:
         return False
      return True

   def save_copy(self, perm_copy):
      if not self.check_num_valid(perm_copy.val):
         return 3
      self.val = perm_copy.val
      return 0

   def save_num(self, n):
      if not self.check_num_valid(n):
         return 3
      self.val = n
      return 0

   #get_status(): call after init, returns status of initialization
   #-1 = uninitialized status, 0 = success
   #1 = one of characters in string or items in array is invalid
   #2 = invalid data type passed to constructor. Can only be list, str, int or Perm
   #3 = check_num_valid() returned False. mostly means that save_copy or save_num got bad data, but also
   #    used in save_str and save_arr
   #4 = uninitialized val
   def get_status(self):
      return self.status

   def __init__(self, item):
      self.status = -1
      self.val = None

      if type(item) is list: #list of Perm objects
         self.status = self.save_arr(item)
      elif type(item) is str: #string format
         self.status = self.save_str(item)
      elif type(item) is Perm: #other perm or one of the capital constants
         self.status = self.save_copy(item)
      elif type(item) is int:
         self.status = self.save_num(item)
      else:
         self.status = 2

      if  self.val is None and (self.status == -1 or self.status == 0):
         self.status = 4

   def has_read(self):
      return (self.val & Perm.READ) is not 0
   def has_write(self):
      return (self.val & Perm.WRITE) is not 0
   def has_admin(self):
      return (self.val & Perm.ADMIN) is not 0
   def has_super_admin(self):
      return (self.val & Perm.SUPER) is not 0

x = Perm([Perm.ADMIN, Perm.SUPER])
x = Perm('asrw')
x = Perm(Perm.ADMIN)
y = Perm(x)

class UserPermissions(dbhelpers.Db):
   #TODO: can make more generic, and each permission is a Tag
   def _init_perm_table(self):
      self.c.execute('''CREATE TABLE perm_groups (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_users (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_group_members (objid integer, group_id integer, user_id integer)''')

      self.c.execute('''CREATE TABLE perm_resources (objid integer, name text)''')
      #group with id group_id has permissions to resource with id resource_id. Perm described in beginning
      self.c.execute('''CREATE TABLE perm_resource_allowed_groups (resource_id integer, group_id integer, perms text)''')

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
      #rid = self._get_rid(rid,) #kkyy
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
#import lock
n = 0
@app.route('/', methods=['POST'])
def on_req():
   global n
   form_db = FormDb()
   f = request.form['name']
   print(f)
   n = n + 1
   #lock.get_id(n)
   db.add_contact(f)
   return 'ok'


#l =
def test_objid():
   for i in urange(0, 1000):
      l = i


