#from asyncio.windows_events import NULL
from dataclasses import replace
#from pynput import keyboard
from flask import Flask, render_template, request, make_response, redirect
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeme'
global m
m=""
@app.route('/')
def index():
    if 'userID' not in request.cookies:
        return render_template('home.html')
    else:
        return redirect('/myfiles')


@app.route('/focused')
def startlisten():
    global m
    m=""
    print("2222222******************hi I was here****************2222222222")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def on_press(key):
    print("******************hi I was here****************")
    global m
    if key==keyboard.Key.esc:
        print(m)
        return False
    try:
        k=key.char
        if(k!="space" and k!="backspace"):
            m+=k
    except:
        k=key.name
        if(k!="space" and k!="backspace"):
            m+=k
    if(k=="space"):
        k=" "
        m+=k
    if(k=="backspace"):
        m = m[:len(m)-1] + "" + m[len(m):]
    

@app.route('/login',methods=['GET','POST'])
def login():
    if 'userID' not in request.cookies:
        if request.method=="GET":
            return render_template('login.html',error="")
        else:
            username=request.form['username']
            password=request.form['password']
            user=user_by_username(username)
            if user:
                if user.password==password:
                    resp = make_response(redirect('/myfiles'))
                    resp.set_cookie('userID', username)
                    return resp
            return render_template('login.html',error="username or password are wrong")
    else:
        return redirect('/myfiles')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if 'userID' not in request.cookies:
        if request.method=="GET":
            return render_template('signup.html',error="")
        else:
            username=request.form['username']
            password=request.form['password'] 
            password2=request.form['password2'] 
            if password2 != password:
                return render_template('signup.html',error="passwords are not the same")
            allusers=query_all()
            for user in allusers:
                if user.username==username:
                    return render_template('signup.html',error="username is already owned by someone else")
            createU(username,password)
            resp = make_response(redirect('/myfiles'))
            resp.set_cookie('userID', username)
            return resp
    else:
        return redirect('/myfiles')
@app.route('/myfiles')
def myfiles():
    name=request.cookies.get('userID')
    if 'userID' in request.cookies:
        print(all_projects_by_user(name))
        if all_projects_by_user(name)==None:
            return redirect('/createProject')
        else:
            all_projects=all_projects_by_user(name)
            return render_template('myfiles.html',username=name,projects=all_projects)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    resp=make_response(redirect('/login')) 
    resp.set_cookie('userID', '', expires=0)
    return resp

@app.route('/createProject',methods=['GET','POST'])
def create_project():
    if 'userID' in request.cookies:
        name=request.cookies.get('userID')
        if request.method=='GET':
            return render_template('createProject.html',errorInside="")
        else:
            project_name=request.form['project_name']
            if create_all_project(project_name,name)=='no good':
                return render_template('createProject.html',errorInside="this project name is already used for this owner")
            return redirect('/myfiles')
    else:
        return redirect('login')


@app.route('/projectPage')
def project_page():
    if 'userID' in request.cookies:
        args=request.args
        id1=args.get('id')
        print(id1)
        files=all_files_by_project(id1)
        shared_users=all_shared_users_by_project(id1)
        project=get_project_by_id(id1)
        return render_template('projectPage.html',files=files,shared_users=shared_users,project=project)
    else:
        return redirect('/login')
@app.route('/share_user',methods=['GET','POST'])
def share_user():
    if 'userID' in request.cookies:
        args=request.args
        id1=args.get('id')
        print(id1)
        if request.method=='GET':
            return render_template('share_user.html',id1=id1)
        else:
            username=request.form['username']
            create_shared_user(id1,username)
            return redirect('/projectPage?id='+id1)
    else:
        return redirect('/login')


@app.route('/deleteShared')
def delete_shared():
    if 'userID' in request.cookies:
        args=request.args
        id1=args.get('id')
        username1=args.get('username')
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        print(username1)
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        if delete_shared_user(username1,id1):
            return redirect('/projectPage?id='+id1)
        else:
            print("FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            return redirect('/projectPage?id='+id1)
    else:
        return redirect('/login')

@app.route('/editprofile',methods=['GET','POST'])
def editprofile():
    if 'userID' in request.cookies:
        name=request.cookies.get('userID')
        user1=user_by_username(name)
        if request.method=='GET':  
            return render_template('editprofile.html',user1=user1,error="")
        else:
            username=request.form['username']
            password=request.form['password']
            password2=request.form['password2']
            users=query_all()

            if password==password2:
                for user in users:
                    if user.username==username:
                        return render_template('editprofile.html',user1=user1,error="username is already owned by someone else")
                edit_user(name,username,password)
                resp = make_response(redirect('/myfiles'))
                resp.set_cookie('userID', username)
                return resp
            return render_template('editprofile.html',user1=user1,error="passwords are not the same")
    else:
        return redirect('/login')
@app.route('/delete_user')
def delete_user():
    if 'userID' in request.cookies:
        args=request.args
        username=args.get('username')
        delete_user_by_username(username)
        resp=make_response(redirect('/login')) 
        resp.set_cookie('userID', '', expires=0)
        return resp
    else:
        return redirect('/login')
    






        

        

            


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

