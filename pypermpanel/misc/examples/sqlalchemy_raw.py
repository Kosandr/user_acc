#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.sql import text

CREDS_PATH = '/sec/creds/mariadb.cred'

user = None
passw = None
with open(CREDS_PATH) as f:
   cred_lines = f.read().split('\n')
   user = cred_lines[0]
   passw = cred_lines[1]

##ECHO is for displaying commands executed
engine_path = 'mysql://%s:%s@localhost/new_db' % (user, passw)
eng = create_engine(engine_path, echo=False)
#con = eng.connect()

def ex1():
   with eng.connect() as con:
      con.execute(text('DROP TABLE IF EXISTS Cars'))
      con.execute(text('CREATE TABLE Cars(Id INTEGER PRIMARY KEY, Name TEXT, Price INTEGER)'''))

      data = ({'Id' : 1, 'Name' : 'Audi', 'Price': 52642 },
              {'Id' : 2, 'Name' : 'Skoda', 'Price' : 8000 })

      for line in data:
         con.execute(text("""INSERT INTO Cars(Id, Name, Price)
                             VALUES(:Id, :Name, :Price)"""), **line)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
class User(Base):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True)
   name = Column(String(length=35))
   fullname = Column(String(35))
   password = Column(String(35))

   def __repr__(self):
      return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
   __tablename__ = 'addresses'
   id = Column(Integer, primary_key=True)
   email_address = Column(String(30), nullable=False)

   user_id = Column(Integer, ForeignKey('users.id')) #constrains user_id to Users.id

   #link Address to User, using attribute Address.user
   user = relationship('User', back_populates='addresses')

   def __repr__(self):
      return "<Address(email_address='%s')>" % self.email_address

#populates Address.user
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

user_ed = User(name='ed', fullname='Ed Jones', password='edspass')
jack = user_ed
jack.addresses = [Address(email_address='jack@google.com'), Address(email_address='j25@yahoo.com')]

print(jack.addresses[1])
print(jack.addresses[1].user)

######JOINTS
#not real join
for u, a in session.query(User, Address).\
      filter(User.id==Address.user_id).\
      filter(Address.email.email_address=='jack@google.com').all():
   print(u)
   print(a)

query = session.query(User)
#real joint, works because we have exactly 1 foreign_key
query(User).join(Address).filter(Address.email_address='jack2google.com').all()
query.join(Address, User.id==Address.user_id) #explicit condition
query.join(User.addresses) #specify relationship from left to right
query.join(Address, User.addresses) #same, with explicit target
query.join('addresses') #same, using string

######OUTER JOINT
query.outerjoin(User.addresses) #left outer join

###########################
#import sqlalchemy_raw
#sqlalchemy_raw.__table__

Base.metadata.create_all(eng) #creates User in database

#########each thread needs it's own session
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=eng)

#alternative initialization in case we don't have engine yet
#Session = sessionmaker()
#Session.configure(bind=eng)

session = Session()

user_bob = User(name='bob', fullname='Bob Jones', password='bobpass')
user_bob2 = User(name='bob2', fullname='Bob Jones', password='bobpass')

#not yet flushed until we do commit
session.add_all([user_ed, user_bob, user_bob2])

#can also do this instead:
#session.add(user_ed)
#session.add(user_bob)

our_user = session.query(User).filter_by(name='ed').first()
print(our_user)

our_user = session.query(User).filter(User.name.in_(['Jo', 'Bah'])).all()
print(our_user)

for instance in session.query(User).order_by(User.id):
   print(instance.name, instance.fullname)

#only works when you session.add() and then modify the object afterwards
#session.dirty = prints bad table
our_user = User(name='bleh')
session.add(our_user)

session.commit() #goes to database

new_user = User(name='test', fullname='blah')
print(new_user in session) #False
session.add(new_user)
print(new_user in session) #True

our_user.name = 'blah'

session.rollback() #undoes the last 3 lines

print(new_user in session) #False

