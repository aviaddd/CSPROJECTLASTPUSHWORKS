from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# TODO: Add your models below this line!
class User(Base):
	__tablename__='users'
	id = Column(Integer, primary_key=True)
	username=Column(String)
	password=Column(String)

class Project(Base):
	__tablename__='projects'
	id = Column(Integer,primary_key=True)
	project_name=Column(String)
	owner=Column(String)

class File(Base):
	__tablename__='files'
	id = Column(Integer,primary_key=True)
	file_name=Column(String)
	project_id=Column(String)

class SharedUser(Base):
	__tablename__='sharedusers'
	id = Column(Integer,primary_key=True)
	project_id=Column(Integer)
	username=Column(String)







