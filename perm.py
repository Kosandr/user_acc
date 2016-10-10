import sqlite3, atomicid, os.path
from flask import Flask, request, send_from_directory
import dbhelpers

app = Flask(__name__)
DB_PATH = '/tmp/permtest.db'

######################Perm
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

'''
x = Perm([Perm.ADMIN, Perm.SUPER])
x = Perm('asrw')
x = Perm(Perm.ADMIN)
y = Perm(x)
'''

#users and groups need to be unique
class UserPermissions(dbhelpers.Db):
   #TODO: can make more generic, and each permission is a Tag
   def _init_perm_table(self):
      #TODO: remove this logic
      #if self.check_if_table_exists('perm_groups'):
      #   return

      self.c.execute('''CREATE TABLE perm_groups (objid integer, name text)''')
      self.c.execute('''CREATE TABLE perm_users (objid integer, name text)''')
      self.c.execute('CREATE TABLE perm_group_members (objid integer, group_id integer, user_id integer)')

      self.c.execute('''CREATE TABLE perm_resources (objid integer, name text)''')

      #group with id group_id has permissions to resource with id resource_id. Perm described in beginning
      self.c.execute('''CREATE TABLE perm_resource_allowed_groups
                                     (objid integer, resource_id integer, group_id integer, perms integer)''')

   def __init__(self, dbpath):
      #tname = 'perm'
      tname = 'perm_groups'
      self.tables_need_exist[tname] = self._init_perm_table
      super(UserPermissions, self).__init__(dbpath)
      #self.init_tables()

   def _get_gid(self, gname):
      self.c.execute('SELECT objid FROM perm_groups WHERE name = ?', (gname, ))
      gid = self.c.fetchone()
      if gid is None:
         return None
      return gid[0]

   def _get_uid(self, uname):
      self.c.execute('SELECT objid FROM perm_users WHERE name = ?', (uname, ))
      uid = self.c.fetchone()
      if uid is None or ((type(uid) is tuple) and uid[0] is None):
         return None
      return uid[0]

   #1 = success, 2 = failure already exists, 3 = failure bad name (short at least 4 chars)
   def new_user(self, uname):
      if len(uname) < 4:
         return 3
      if self._get_uid(uname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_users VALUES (?, ?)', (self.get_obj_id(), uname))
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
   def new_group(self, groupname):
      if self._get_gid(groupname) is not None:
         return 2
      self.c.execute('INSERT INTO perm_groups VALUES (?, ?)', (self.get_obj_id(), groupname))
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
   def add_user_to_group(self, groupname, uname):
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

      self.c.execute('INSERT INTO perm_group_members VALUES (?, ?, ?)', (self.get_obj_id(), gId, uId))
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

   def _get_permid_by_ids(self, res_id, group_id):
      self.c.execute('''SELECT objid FROM perm_resource_allowed_groups WHERE
                           group_id = ? AND resource_id = ?''', (group_id, res_id))
      pid = self.c.fetchone()
      if pid is None or (type(pid) is tuple and pid[0] is None):
         return None
      return pid[0]

   def _get_permid_by_names(self, res_name, group_name):
      self.c.execute('''SELECT objid FROM perm_resource_allowed_groups WHERE
                           group_id = ? AND user_id = ?''', (gid, uid))
      return

   #new_resource(res_name)
   #1 = success
   #2 = resource already exists
   #3 = one of groups doesn't exist
   #declare resource, and its access rights
   def new_resource(self, res_name): #, groups=[]):
      rid = self._get_rid(res_name)
      if rid is not None:
         return 2
      rid = self.get_obj_id()
      self.c.execute('INSERT INTO perm_resources VALUES (?, ?)', (rid, res_name))

      #for group in groups:
      #   ret = self.perm_resource_add_group(group)
      #   if ret != 1:
      #      return ret
      return 1

   #1 = success
   #2 = res_name resource doesn't exist, 3 = group_name doesn't exist
   #4 = (4, 'bad_perm', perm_init_status) #whenever perms passed are invalid
   #5 = record for this group/resource combo should exist, but can't find it
   def resource_group_add_perms(self, res_name, group_name, perms, remove_old=False):
      #rid = self._get_rid(rid,) #kkyy
      rid = self._get_rid(res_name)
      if rid is None:
         return 2
      gid = self._get_gid(group_name)
      if gid is None:
         return 3

      real_perm = Perm(perms)
      if real_perm.get_status() != 0:
         return (4, 'bad_perm', real_perm.get_status())

      pid_old_entry = self._get_permid_by_ids(rid, gid)
      if pid_old_entry is None:
         pid = self.get_obj_id() #permission id
         arg_tuple = (pid, rid, gid, real_perm.val)
         self.c.execute('INSERT INTO perm_resource_allowed_groups VALUES (?, ?, ?, ?)', arg_tuple)
      else:
         if not remove_old:
            self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE objid = ?',
                                   (pid_old_entry, ))
            perms = self.c.fetchone()
            if perms is None or ((type(perms) is tuple) and  perms[0] is None):
               return 5
            old_perms = Perm(int(perms[0]))
            real_perm = Perm(real_perm.val | old_perms.val)

         self.c.execute('DELETE FROM perm_resource_allowed_groups WHERE objid = ?',
                        (pid_old_entry, ))

         arg_tuple = (pid_old_entry, rid, gid, real_perm.val)
         self.c.execute('INSERT INTO perm_resource_allowed_groups VALUES (?, ?, ?, ?)', arg_tuple)
      self.conn.commit()
      return 1

      #self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE')
   def resource_group_rm_perms(self, perm_id, perms): #(res_name, group_name):
      pass

   def resource_group_drop_all_perms(self, perm_id): #resource_group_rm_all_perms()
      pass

   #1 = success, 2 = res_name doesn't exist, 3 = group_name doesn't exist
   #4 = (4, 'bad_perm', perm_init_status)
   #5 = record for this group/res combo should exist but can't find it
   def get_resource_group_perms(self, res_name, group_name):
      rid = self._get_rid(res_name)
      if rid is None:
         return 2
      gid = self._get_gid(group_name)
      if gid is None:
         return 3

      pid = self._get_permid_by_ids(rid, gid)
      if pid is None:
         return Perm(0)
      else:
         self.c.execute('SELECT perms FROM perm_resource_allowed_groups WHERE objid = ?',
                                (pid, ))
         perms = self.c.fetchone()
         if perms is None or ((type(perms) is tuple) and  perms[0] is None):
            return 5
         perms = Perm(int(perms[0]))
         if perms.get_status() != 0:
            return (4, 'bad_perm', perms.get_status())
         return perms


   #def modify_resource_rights(res_name):
   #   pass

   #decorator. Passes arg "allowed"
   def resource_name(name):
      pass


'''UserPermissions example
from perm import UserPermissions
p = UserPermissions('/sec/db/dbtnext/usertest.db')

p.new_group('viewer')
p.new_group('writer')
p.new_group('privaleged_viewer')
p.new_group('privaleged_modifier')
p.new_group('admin')

#main user
p.new_user('root')
p.new_group('root')
p.add_user_to_group('root', 'root')
p.add_user_to_group('admin', 'root')

#approve section
p.new_resource('approve_section')
p.resource_group_add_perms('approve_section', 'root', 'ws') #'ws'
p.resource_group_rm_perms('approve_section', 'admin', 'rw') #'rws'
p.resource_group_rm_perms('approve_section', 'admin', 'wa', True) #resets, so 'wa' and no 's' or 'r'

p.get_resource_group_perms('approve_section', 'root')

#@requires_group('admin')
@p.resource_name('approve_section')
def approve_user(uname):
   pass

#@requires_group('admin')
@p.resource_name('modify_user_group')
def add_user_to_group(uname, grp):
   pass

@p.resource_name('report')
def get_report(reportname):
   pass

#def view_report():
#   pass
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


