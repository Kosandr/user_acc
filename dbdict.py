

class DbDict:
   def __init__(self, db_path):
      self.db_path = db_path

     if not os.path.exists(db_path):
         need_init = True

      self.conn = sqlite3.connect(DB_PATH)
      self.c = self.conn.cursor()

      if need_init:
         self.init_db()

   def init_db():
      create_str = 'CREATE VIRTUAL TABLE %s USING fts4'
      create_str = 'CREATE TABLE %s'

      self.c.execute('''%s (key string, val string)''' % (create_str % 'str_str')

      #TODO: using whole string just to store integer? bad idea
      self.c.execute('''CREATE VIRTUAL TABLE str_int USING fts4
                           (key string, val integer)''')

      self.c.execute('''CREATE VIRTUAL TABLE int_str USING fts4
                           (key integer, val string)''')

      self.c.execute('''CREATE VIRTUAL TABLE int_int USING fts4
                           (key integer, val integer)''')
      self.conn.commit()

   def set(key, val):
      self.c.execute('SELECT



