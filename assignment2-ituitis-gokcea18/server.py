import os

from pathlib import Path
from bottle import static_file ,Bottle,route, request

from hash_passwd import create_hash
hashed = "0116ede46f8330ca4144d71bc3bc6dc5d6be61543cf2da1c077057f674f4c085"

UserList_Dict = []
UserTable = ""

def UpdateTable():
    global UserTable
    templateTable = ""
    for User in UserList_Dict:
        templateRow = """
        <tr>
            <td>%(ip)s</td>
            <td>%(count)d</td>
        </tr>
        """ % {"ip": User.get("IP"),"count":User.get("Count")}
        templateTable += templateRow
    UserTable = templateTable
    return

def ResetTable():
    UserList_Dict.clear()
    return

def IncreaseCount(User):
    x = User.get("Count")
    User["Count"] = x+1
    return

def addUser2List(ip):
    newUser = {}
    if not UserList_Dict: ###if list is empty
        newUser = {"IP":ip,"Count":1}
        UserList_Dict.append(newUser)
        UpdateTable()
        return
    else:
        for User in UserList_Dict: ###if list contains that ip
            if User.get("IP") == ip:
                IncreaseCount(User)
                UpdateTable()
                return
        newUser = {"IP":ip,"Count":1} ###if list doesnt contains that ip
        UserList_Dict.append(newUser)
        UpdateTable()
        return

def home_page():
    IP = request.headers.get("X-Forwarded-For", "127.0.0.1")
    addUser2List(IP)
    content = Path("index.html").read_text() % {"Table":UserTable}
    return content

def about_page():
    return Path("about.html").read_text()

def contact_page():
    return Path("contact.html").read_text()

def pwdChechker(pwd):
    pwdHash = create_hash(pwd)
    if pwdHash == hashed:
        return True
    else:
        return False       

def reset_page():
    content = Path("password.html").read_text()
    entriedPassword = request.POST.get("pwd")
    confirm = request.POST.get("confirm")
    if(pwdChechker(entriedPassword)):
        ResetTable()
        return content % {"message":"Users have succesfully deleted"}
    else:
        return content % {"message":"Wrong password please try again"}
        

def server_static(path):
    return static_file(path, root='.')

def create_app():
    app = Bottle()
    app.route("/", "GET", home_page)
    app.route("/index.html", ["GET","POST"], home_page)
    app.route("/about.html", "GET", about_page)
    app.route("/contact.html", "GET", contact_page)
    app.route("/passwordChecker", "POST", reset_page)
    app.route('/static/<path>', 'GET', server_static)
    return app


application = create_app()
application.run(debug=True, host="0.0.0.0",port=int(os.environ.get("PORT", 8080)))
