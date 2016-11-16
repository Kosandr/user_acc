import os.path, sqlite3

#types: number, text

class DbHelper(object):
   def __init__(self, path):
      self.conn = sqlite3.connect(path) #, check_same_thread=False)
      self.c = self.conn.cursor()

   def check_if_table_exists(self, tableName):
      self.c.execute('''SELECT name FROM sqlite_master
                        WHERE type='table' AND name=?''', (tableName,))
      ret = self.c.fetchone()
      if ret is None:
         return False
      else:
         return True


   def init_if_no_db(self, db_path, init_f):
      if not os.path.exists(db_path):
         self.init_f(self.conn, self.c, db_path)

   #fields = [(name, type), (name, type)]
   def create_table(self, name, fields, use_fts=True):
      if use_fts:
         init_str = 'CREATE VIRTUAL TABLE '
      else:
         init_str = 'CREATE TABLE '

      init_str += name

      if use_fts:
         init_str += ' USING fts4'
      init_str += ' ('

      for field in fields:
         init_str += field[0] + ' ' + field[1] + ', '
      init_str = init_str[:-2]
      init_str += ');'


      print(init_str)
      return

      self.c.execute(init_str)

DB_PATH = '/sec/db/dbtnext/formdata.db'

class FormDb(DbHelper):
   def init_empty_db(self):
      table_entries = [
         ('FormId', 'number'), ('first_name', 'text'), ('last_name', 'text'),
         ('spouse_first_name', 'text'), ('spouse_last_name', 'text'),
         ('email', 'text'), ('json_data_origin', 'text')
      ]

      self.create_table('surveys', table_entries, False)

   def __init__(self):
      super(FormDb, self).__init__(DB_PATH)

      self.init_empty_db()
      #self.init_if_no_db(


if __name__ == '__main__':
   x = FormDb()



