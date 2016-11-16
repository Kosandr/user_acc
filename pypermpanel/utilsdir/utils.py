from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
import datetime

_boolc = Column(Boolean)
_intc = Column(Integer)
_floatc = Column(Float)
_idc = Column(Integer, primary_key=True)
_textc = Column(Text)
_datetimec = Column(DateTime)

def idc():
   return Column(Integer, primary_key=True) #_idc
def boolc():
   return Column(Boolean) #_boolc
def intc():
   return Column(Integer) #_intc
def floatc():
   return Column(Float) #_floatc
def textc():
   return Column(Text) #_textc
def stringc(length=None):
   return Column(String(length=length))
def datetimec():
   return Column(DateTime) #_datetimec
def foreignidc(key):
   return Column(Integer, ForeignKey(key))

class Maybe:
   def __init__(self, val, err_code=None):
      self.val = val
      self.err_code = err_code

   def is_good(self):
      return self.err_code is None
   def is_err(self):
      return self.err_code is not None
   def get_val(self):
      return self.val
   def get_err(self):
      return self.val
   def get_err_code(self):
      return self.err_code

   def __repr__(self):
      ret = '<Maybe is_err=' + str(self.is_err()) + ' '
      if self.is_err():
         ret += ' err_code=' + str(self.err_code)
      ret += ' ret={' + repr(self.val) + '}'
      ret += '>'
      return ret


class AlchemyConfig:
   def __init__(self, eng = None, session = None, Session = None, debug = False):
      self.eng = eng
      self.session = session
      self.Session = Session
      self.debug = debug

   def from_engine_path(engine_path, debug=False, pool_recycle=None):
      if pool_recycle is None:
         pool_recycle = 3600
      eng = create_engine(engine_path, echo=debug, pool_recycle=pool_recycle)
      Session = sessionmaker(bind=eng)
      session = Session()

      return AlchemyConfig(eng, session, Session, debug=debug)

   def from_eng_sesh(eng, sesh, debug=False):
      return AlchemyConfig(eng, sesh, debug=debug)

   def from_creds(uname, passw, db_name, db_backend='mysql', debug = False):
      engine_path_args = (db_backend, uname, passw, db_name)
      engine_path = '%s://%s:%s@localhost/%s' % engine_path_args
      return AlchemyConfig.from_engine_path(engine_path)

   #first line uname, second line password
   def from_creds_file_path(creds_path, db_name, debug = False):
      user, passw = AlchemyConfig.get_mariadb_creds(creds_path)
      return AlchemyConfig.from_creds(user, passw, db_name, debug = debug)

   def get_mariadb_creds(creds_path):
      user = None
      passw = None
      with open(creds_path) as f:
         cred_lines = f.read().split('\n')
         user = cred_lines[0]
         passw = cred_lines[1]
      return user, passw

def try_to_float(s, default=None):
   try:
      return float(s)
   except:
      return default

def try_to_int(s, default=None):
   try:
      return int(s)
   except:
      return default

#enum_arg = string in enum_list or int index in enum_list
def enum_helper(enum_list, enum_arg, to_index=None):
   options = [x.lower() for x in enum_list]

   if to_index is None:
      if enum_arg is None:
         return None
      elif type(enum_arg) is str:
         to_index = True
      elif type(enum_arg) is int:
         to_index = False
      else:
         raise "Bad type passed to utils.enum_helper(%s)" % (str(enum_arg))

   try:
      if to_index:
         return options.index(enum_arg.lower())
      else:
         return options[enum_arg]
   except Exception as e:
      pass
   return None

import time, datetime

def datetime_to_unix(d):
   return time.mktime(d.timetuple())

def unix_to_datetime(x):
   return datetime.datetime.fromtimestamp(int(x))

def datetime_to_str(d):
   return d.strftime('%Y-%m-%d %H:%M:%S')


