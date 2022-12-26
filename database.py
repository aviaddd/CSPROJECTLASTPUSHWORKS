from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# TODO: Add your database functions below this line!
def createU(username,password):
	user1=User(username=username,password=password)
	session.add(user1)
	session.commit()

def query_all():
	return session.query(User).all()

def	user_by_username(username):
	return session.query(User).filter_by(username=username).first()

def all_projects_for_owner(owner):
	return session.query(Project).filter_by(owner=owner).all()

def all_projects():
	return session.query(Project).all()




def all_shared_projects_by_user(username):
	return session.query(SharedUser).filter_by(username=username).all()

def project_by_id(project_id):
	return session.query(Project).filter_by(id=project_id).first()




def all_projects_by_user(username):
	allprojectslist=all_projects_for_owner(username)
	print(allprojectslist)
	shareds=all_shared_projects_by_user(username)
	for shared in shareds:
		allprojectslist.append(project_by_id(shared.project_id))
	return allprojectslist

def get_project_by_name(project_name,owner):
	all_projects=all_projects_for_owner(owner)
	for project in all_projects:
		if project.project_name==project_name:
			return project
	return "no such filename for owner"

def get_project_by_id(project_id):
	return session.query(Project).filter_by(id=project_id).first()

def create_project(project_name, owner):
	project1=Project(project_name=project_name,owner=owner)
	session.add(project1)
	session.commit()

def create_all_project(project_name,owner):
	all_projects=all_projects_for_owner(owner)
	for project in all_projects:
		if project.project_name==project_name:
			return 'no good'
	create_project(project_name,owner)
	all_projects=all_projects_for_owner(owner)
	project=get_project_by_name(project_name,owner)
	create_file('script',project.id)
	create_file('script2',project.id)
	create_file('script3',project.id)
	return 'this good'

def all_files_by_project(project_id):
	return session.query(File).filter_by(project_id=project_id).all()

def create_file(file_name,project_id):
	file1=File(file_name=file_name,project_id=project_id)
	session.add(file1)
	session.commit()


def all_shared_users():
	return session.query(SharedUser).all()

def create_shared_user(project_id,username):
	shared1=SharedUser(project_id=project_id,username=username)
	session.add(shared1)
	session.commit()

def all_shared_users_by_project(project_id):
	return session.query(SharedUser).filter_by(project_id=project_id).all()

def delete_shared_user(username,project_id):
	shareds=all_shared_users_by_project(project_id)
	print (shareds)
	for shared in shareds:
		print("HIIIIIIIIIIIIIIIIIIIIIII")
		print(shared.project_id)
		print (shared.username)
		if shared.username==username:
			session.delete(shared)
			session.commit
			return True
	return False
		
def user_by_username(username):
	return session.query(User).filter_by(username=username).first()

def edit_user(old_username,new_username,password):
	user=session.query(User).filter_by(username=old_username).first()
	user.username=new_username
	user.password=password
	session.commit()

def delete_user_by_username(username):
	session.delete(session.query(User).filter_by(username=username).first())
	session.commit()