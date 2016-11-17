


###coding notes:
#D# = commented out debug code

#############
deps: jsx/react, redis, sqlite3, mariadb
python deps:
   pip install libsass, flask
   pip binding for sqlite3

sudo npm install -g browserify
#############

#sass
sudo pip3 install libsass sh

#react jsx:
sudo apt-get install nodejs-legacy
npm install --save-dev -g babel-cli babel-preset-latest
npm install babel-plugin-transform-react-jsx

#for safari
npm install --save-dev babel-preset-es2015
#add this for es2015 to .babelrc:
#{"presets": ["es2015"]}
#https://babeljs.io/docs/plugins/preset-es2015/
#http://stackoverflow.com/questions/33821312/how-to-remove-global-use-strict-added-by-babel

#npm install react react-dom #optional
babel --plugins transform-react-jsx test.jsx >test.js


pip install Flask-Session

pip install redis
sudo apt-get install redis-server


sudo apt-get install software-properties-common
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://mariadb.mirror.anstey.ca/repo/10.1/ubuntu xenial main'

sudo apt update
sudo apt install mariadb-server


sudo apt-get install libmariadbclient-dev
sudo apt-get install python-mariadb
sudo apt-get install python-mysqldb


sudo pip3 install SQLAlchemy
#sudo pip3 install MySql-Python #doesn't support python3
pip install mysqlclient #instead of MySql-Python

========================misc/notes.txt
===python production
http://docs.gunicorn.org/en/latest/deploy.html
http://nginx.org/en/docs/http/ngx_http_upstream_module.html

gunicorn
   sudo pip3 install gunicorn
   gunicorn serv:app
      --workers=5
      --bind=4220 #port
   ex
      gunicorn serv:app --workers=5 --bind=4220
         #app is object, serv is package

===end python production

==============sqlalchemy
TODO: read "Using Textual SQL" starting on "Bind paramters" sentence

links:
   SQL Expression Language
   http://docs.sqlalchemy.org/en/rel_1_1/core/tutorial.html
   ORM (Object Relations Mapping)
      http://docs.sqlalchemy.org/en/rel_1_1/orm/tutorial.html

filter/query/limit
   Query returns named tuples (KeyedTuple)
   Query supports ORM-instrumented descriptors
   common filters
      EQUALS      = query.filter(User.name == 'ed')
      NOT EQUALS  = query.filter(User.name != 'ed')
      LIKE        = query.filter(User.name.like('%ed%'))
      IN          = query.filter(User.name.in_(['ed', 'wendy']))
      IN #2       = query.filter(User.name.in_(
                      session.query(User.name).filter(User.name.like('%ed%'))
                    ))
      NOT IN      = query.filter(~User.name.in_(['ed', 'wanda']))
      IS NULL     = query.filter(User.name == None) or query.filter
                    query.filter(User.name.is_(None))
      IS NOT NULL = query.filter(User.name != None)
                    query.filter(User.name.isnot(None))
      AND         = from sqlalchemy import and_
                    query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
                    query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
                    query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
      OR          = from sqlalchemy import or_
                    query.filter(or_(User.name == 'ed', User.name == 'wendy'))
      MATCH/CONTAINS
                  = query.filter(User.name.match('wendy'))

   ex 1 filter_by (used with keyboards):
      our_user = session.query(User).filter_by(name='ed').first()
   ex 2 filter (magic operator without lambda):
      our_user = session.query(User).filter(User.name == 'Ed')
      our_user = session.query(User).filter(User.name.in_(['Ho', 'Bah'])).all()`
   ex 3 (LIMIT/OFFSET/ORDER BY):
      for u in session.query(User).order_by(User.id)[1:3]:
         print(u)
   ex 4:
      for instance in session.query(User).order_by(User.id):
         print(instance.name, instance.fullname)`
   ex 5:
      for row in session.query(User, User.fullname, User.name).all():
         print(row.User, row.name, row.fullname)
   ex 6 (with labels):
      for row in session.query(User.name.label('name_label')).all():
         print(row.name_label)
   ex 7 aliases:
      from sqlalchemy.orm import aliased
      user_alias = aliased(User, name='user_alias')
      for row in session.query(user_aliases, user_aliases.name).all():
         print(row.user_alias)
   ex 8 generative (uses AND):
      for user in session.query(User).\
            filter(User.name=='ed').\
            filter(User.fullname=='Ed blah'):
         print(user)

returning lists and scalars
   ex:
      query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
      query.all() #gets all
      query.first() #applies limit of 1
      query.one() #fully fetches all rows, and if not exactly 1 object found, raises an error
      query.one_or_none() #if more than one, still raises
      query.scalar() #invokes one(), and upon success returns the first column of row
         session.query(User.id).filter(User.name == 'ed').order_by(User.id).scalar() #returns id

textual queries:
   ex1:
      from sqlalchemy import text
      for user in session.query(user).filter(text("id<224")).order_by(text("id")).all():
         print(user.name)
   bind paramaters:
      session.query(User).filter(text("id<:value and name=:name")).\
         params(value=224, name='fred').order_by(User.id).one()
   entire text query:
      session.query(User).from_statement(
         text("SELECT * FROM users where name=:name")).\
         params(name='ed').all()
      #returns list of User objects
   TextClause (if doesn't map very well idk what exactly for):
      stmt = text("SELECT name, id, fullname, password "
                  "FROM users where name=:name")
      stmt = stmt.columns(User.name, User.id, User.fullname, User.password)
      session.query(User).from_statement(stmt).parmas(name='ed').all()
      #returns User object???
   text specify which to return
      stmt = text("SELECT name, id FROM users where name=:name")
      stmt = stmt.columns(User.name, User.id)
      session.query(User.id, User.name)
      #returns [(1, u'ed')]

`counting:
   creates sub-query and then does "SELECT count(*) FROM table"
      session.query(User).filter(User.name.like('%ed')).count()
   when "thing to be counted" needs to be explicit
      from sqlalchemy import func
      session.query(func.count(User.name), User.name).group_by(User.name).all()
         => [(1, u'ed'), (1, u'fred')]
   first method using second method (to achieve SELECT count(*) FROM table)
      session.query(func.count('*')).select_from(User).scalar() #returns integer
   same thing without select_from()
      session.query(func.count(User.id)).scalar()`

`relationships:
ex1:

`

==============mariadb notes
links:
   adding primary keys later on
      https://mariadb.com/kb/en/mariadb/getting-started-with-indexes/
   joins
      https://mariadb.com/kb/en/mariadb/introduction-to-joins/
types:
   VARCHAR(strlen) = VARCHAR(10)
   CHAR
   INT
   BLOB = up to 65,535 bytes
   LONGBLOG = Blob up to 4GB
   TINYTEXT = text up to 255 chars
   TEXT = up to 65,535
   MEDIUMTEXT = 16,777,215
   LONGTEXT 4,294,967,295

==login/misc
login
   mysql -u root -p
create db
   CREATE DATABASE newdb;
   CREATE DATABASE IF NOT EXIST newdb;
drop db
   DROP DATABASE newdb;
   DROP DATABASE IF EXISTS newdb;
create table
   CREATE TABLE table2 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Title VARCHAR(100) NOT NULL, AuthorID INT);
   CREATE TABLE IF NOT EXISTS test_table (id INT PRIMARY KEY);
show
   SHOW DATABASES;
   SHOW TABLES;
describe
   DESCRIBE <TABLENAME>;
use = specify current db being used
   USE dbname;
specify database
   SELECT database();
   USE new_database;
   SELECT database(); #this is now new_db
insert
   INSERT INTO <tablename> VALUES (1, 'Test');
select
   SELECT id, name FROM <tablename> WHERE id = 1;
   SELECT * FROM <tablename>;
update
   UPDATE <tablename> SET name = 'Blah' WHERE id = 1;
delete
   DELETE FROM <tablename> WHERE id = 1;
drop
   DROP DATABASE <dbname>;

autoincrement example:
   CREATE DATABASE test;
   USE test;
   CREATE TABLE IF NOT EXISTS books (BookID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Title VARCHAR(100) NOT NULL, AuthorID INT);
   INSERT INTO books (Title, AuthorId) VALUES ('Test', 15);

example usage:
   CREATE DATABASE mydb;
   USE mydb;
   CREATE TABLE mytable (id INT PRIMARY KEY, name VARCHAR(20));

   INSERT INTO mytable VALUES(1, 'Will');
   INSERT INTO mytable VALUES(2, 'Marry');
   SELECT id, name FROM mytable WHERE id = 1;
   UPDATE mytable SET name = 'Willy' WHERE id = 1;
   SELECT id, name FROM mytable;
   DELETE FROM mytable WHERE id = 1;
   DROP DATABASE mydb;
   SELECT count(1) from mytable;

================other notes
===dpkg/apt
list installed packages
   dpkg --get-selections | grep -v deinstall
   dpkg-query -l
   apt list --installed
===python
reload module
   import imp
   imp.reload(loade_module)
===tmux
cheatsheet
   https://gist.github.com/MohamedAlaa/2961058
disconnect old client and attach
   tmux -dt <session>
   http://stackoverflow.com/questions/22138211/how-do-i-disconnect-all-other-users-in-tmux
   when freezes and then re-attach but it acts like old one is still attached
===vim
links
   http://vim.wikia.com/wiki/Syntax_folding_of_Vim_scripts
   http://vim.wikia.com/wiki/Folding
set folding modes
   :setlocal foldingmethod={manual/indent/syntax/expr}
renew syntax highlights
   :syn sync fromstart
re-open window closed with :q or when you open another window over it
   :e#
===sshfs
syntax
   sshfs kkostya@familyape.com:/ /tmp/serv
===kdate
prints time in am/pm format
   echo `date +"%I:%M %p"`
/usr/bin/kdate:
   #!/bin/bash
   echo `date +"%I:%M %p"`
===

