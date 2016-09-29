from multiprocessing import Lock
import time, sqlite3, os.path

lock = Lock()

class ObjId:
   def __init__(self, dbpath):
      need_init = False
      if not os.path.exists(dbpath):
         need_init = True

      self.conn = sqlite3.connect(dbpath)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

   def init_db(self):
      lock.acquire()
      self.c.execute('''CREATE TABLE obj_ids (objindex integer)''')
      self.c.execute('''INSERT INTO obj_ids VALUES (0)''')
      self.conn.commit()
      lock.release()

   def get_id(self):
      lock.acquire()
      self.c.execute('''SELECT objindex FROM obj_ids''')
      ret = self.c.fetchone()[0]
      pair = (ret+1, ret)
      self.c.execute('''UPDATE obj_ids SET objindex=? where objindex=?''', pair)
      self.conn.commit()
      lock.release()
      return ret

