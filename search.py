
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY']="ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
items = [
    {"title" : "Arduino uno", "url" : "image_1.png", "html" : "<p>Arduino Uno content</p>"},
    {"title" : "Driver Board", "url" : "imagev3board.png", "html" : "<p>Driver Board content</p>"},
    {"title" : "High Power DCDC", "url" : "imagedcdc2.png", "html" : "<p>High Power DCDC content</p>"},
    {"title" : "VGA connector", "url" : "imagevgaconnector.png", "html" : "<p>VGA connector content</p>"},
    {"title" : "Xbee", "url" : "imagexbee.png", "html" : "<p>Xbee content</p>"},

]

@app.route("/")
def index():
    global items
    username = session.get("user", None)
    if username is None:
        return redirect("/auth")
    return render_template("online_project_arduino2.html", items=items)


@app.route("/detail")
def detail():
    global items
    i = 0
    if "id" in request.args:
        i = int(request.args["id"])
    item = items[i]
    return render_template("detail.html", item=item)


@app.route("/auth")
def auth():
    msg = ""
    if "msg" in request.args:
        msg = request.args["msg"]
    return render_template("sign_in.html", error_message=msg)


@app.route("/page1")
def page1():
    return render_template("online_project_arduino.html")
@app.route("/page2")
def page2():
    return  render_template("online project arduino part.html")

@app.route("/page3")
def page3():
    return  render_template("online_project_control.html")

# @app.route("/auth")
# def sign_in():
#     msg = ""
#     if "msg" in request.args:
#         msg = request.args["msg"]
#     return render_template("auth.html", error_message=msg)

@app.route("/login", methods=["GET", "POST"])
def login():
    name = request.form["txt_user"]
    pswd = request.form["txt_pswd"]
    with open("user.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        a, b = line.split(",")
        a = a.strip()
        b = b.strip()
        if name == a and pswd == b:
            session["user"]=name
            return redirect("/")
    return redirect("/sign_in?msg=登入失敗")

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    search = request.form["search"]
    with open("search.txt", "a+") as f:
        f.write(search + "\n")
    return "OK"

app.run(host="0.0.0.0", port=5000, debug=True)