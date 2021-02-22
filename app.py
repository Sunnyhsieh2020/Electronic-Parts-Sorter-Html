from flask import Flask, render_template, request, redirect, session
import pickle
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"

items = [
    {"item_id": 0, "class_id": 0, "title": "Arduino uno",                           "url": "image_1.png",                              "html": "<p>Arduino Uno content</p>",       "cost": "MOP:195.5","location": "line:1,cabinet:1",            "function": "The Arduino Uno is a microcontroller board based on the ATmega328.It has 20 digital input/output pins","type":"Arduino Uno (R3) Arduino Nano, Arduino Micro, Arduino Due,LilyPad Arduino Board, Arduino Bluetooth, Arduino Diecimila......",                                                                                               "key": ["arduino Uno", "uno", "arduino","arduinouno"]},
    {"item_id": 1, "class_id": 1, "title": "Driver Board",                          "url": "imagedriverboard.png",                     "html": "<p>Driver Board content</p>",      "cost": "MOP:20",   "location": "line:1,cabinet:2",            "function": "It’s easy to use Arduino or other development platform to drive the stepper motor by this diver board.","type":"Input Power Adapter: 12Vdc More than 2A. Board Size: 77mm x 55mm x 16mm.",                                                                                                                                                 "key": ["driver", "board", "driver board","driverboard"]},
    {"item_id": 2, "class_id": 1, "title": "High Power DCDC",                       "url": "imagehighpowerdcdc.png",                   "html": "<p>High Power DCDC content</p>",   "cost": "MOP:22",   "location": "line:1,cabinet:3",            "function": "A DC-to-DC converter is an electronic circuit or electromechanical device that converts a source of direct current (DC) from one voltage level to another. It is a type of electric power converter. ","type":"DC-to-DC converters are subject to different types of chaotic dynamics such as bifurcation, crisis, and intermittency.",    "key": ["high","power","dcdc","high power","high power dcdc","highpowerdcdc"]},
    {"item_id": 3, "class_id": 2, "title": "VGA connector",                         "url": "imagevgaconnector.png",                    "html": "<p>VGA connector content</p>",     "cost": "MOP:72",   "location": "line:1,cabinet:4",            "function": "A VGA cable is a device used to transfer video signals. It does this by acting as a link between the computer and the monitor or between the computer and the television screen. The video graphic cable comes in two types, male and female connector.","type":"Operating Voltage  3.3V to 5.5V, Board Dimensions" ,                     "key": ["vga connector", "vga","connector"]},
    {"item_id": 4, "class_id": 2, "title": "Xbee",                                  "url": "imagexbee.png",                            "html": "<p>Xbee content</p>",              "cost": "MOP:167",  "location": "line:2,cabinet:1",            "function": "This shield V03 can achieve a simple two crunodal ZigBee network achieve wireless communication between Arduino, and allows the Arduino to wireless communicate over a modified ZigBee protocol using the popular XBee module.",                                                                                                           "key": []},
    {"item_id": 5, "class_id": 2, "title": "CH376S_USB",                            "url": "imagech376s.png",                          "html": "<p>CH376S USB content</p>",        "cost": "MOP:56",   "location": "line:2,cabinet:2",            "function": "CH376 Function:CH376 is a universal interface chip of USB bus, with 8-bit data bus, read, write, chip control line and interrupt output, which can be easily connected to the system bus of MCU/ DSP/MCU/MPU controller.",                                                                                                                 "key": []},
    {"item_id": 6, "class_id": 0, "title": "CupA S1 Arduino",                       "url": "imagecupa_s1_arduino.png",                 "html": "<p>CupA S1 Arduino content</p>",   "cost": "MOP:48",   "location": "line:2,cabinet:3",            "function": "Magic Light Cup modules are easy to Interactive Technology Division developed a can and ARDUINO interactive modules, PWM dimming principle is to use the principle of two modules brightness changes.",                                                                                                                                    "key": []},
    {"item_id" : 7, "class_id" : 1, "title" : "Funduino Joystick",                  "url" : "image_2.png",                             "html" : "<p>Funduino Joystick content</p>", "cost" : "MOP:57.8", "location" : "line:2,cabinet:4",         "function" : "CH376 Function:CH376 is a universal interface chip of USB bus, with 8-bit data bus, read, write, chip control line and interrupt output, which can be easily connected to the system bus of MCU/ DSP/MCU/MPU controller.",                                                                                                                "key" : []},

    {"item_id" : 8, "class_id" : 2, "title" : "Micro Female Seat",                  "url" : "imageMicro_Female_Seat.png",              "html" : "<p>Micro Female Seat content</p>", "cost" : "MOP:8", "location" : "line:3,cabinet:1",             "function" : "MICRO USB transformed into DIP, female seat B type, patch turn into DIP transfer board welded female seat Description: Highlights: MICRO USB is an international standard, most smartphone data lines have adopted this interface, wide range of uses, this module easily be converted to conventional...",                              "key" : []},
    {"item_id" : 9, "class_id" : 2, "title" : "LTC3708 Automatic Buck Boost",       "url" : "imageautomaticbucks.png",                 "html" : "<p>LTC3708 Automatic Buck Boost content</p>", "cost" : "MOP:100", "location" : "line:3,cabinet:2",             "function" : "This power supply is a high efficiency regulated power supply module. Output voltage can keep stable when input voltage  is below, above or  equal to the output voltage.",                                                                                                                                                 "key" : []},
    {"item_id" : 10, "class_id" : 1, "title" : "Proto Shield Expanding Board",      "url" : "imageprtoshield.png",                        "html" : "<p>Proto Shield Expanding Board content</p>", "cost" : "MOP:31.86", "location" : "line:3,cabinet:3",    "function" : "Used in conjunction with the Duemilanove ProtoShield prototype expansion board.With Self-adhesive tape on the back of miniboard, easy to stick on the Arduino Prototype Shield.",   "key" : []},

]

menu = [
    {"class_id": 0, "title": "Arduino",           "html": "click to see more type of Arduino parts",             "url": "image_1.png"},
    {"class_id": 1,"title": "Control & Board",    "html": "click to see more type of Control & Board parts",     "url": "image_2.png"},
    {"class_id": 2,"title": "module & Connector", "html": "click to see more type of Module & Connector parts",  "url": "imageethernet.png"},
]

@app.route("/")
def index():
    global items, menu
    username = session.get("user", None)
    if username is None:
        return redirect("/auth")
    class_id = 0
    if "id" in request.args:
        class_id = int(request.args["id"])
    rs = []
    for item in items:
        if item["class_id"] == class_id:
            rs.append(item)
    bookmark_names = []
    if session.get("bookmark_list") is not None:
        bookmark_names = [x[0] for x in session.get("bookmark_list")]
    bookmark_list = []
    if session.get("bookmark_list") is not None:
        bookmark_list = session.get("bookmark_list")
    return render_template("index.html", menu=menu,items=rs, bookmark_list=bookmark_list, bookmark_names=bookmark_names)   # 所有arduino零件


@app.route("/category")
def category():
    global items, menu
    class_id = 0
    if "id" in request.args:
        class_id = int(request.args["id"])
    rs = []
    for item in items:
        if item["class_id"] == class_id:
            rs.append(item)
    bookmark_names = []
    if session.get("bookmark_list") is not None:
        bookmark_names = [x[0] for x in session.get("bookmark_list")]
    bookmark_list = []
    if session.get("bookmark_list") is not None:
        bookmark_list = session.get("bookmark_list")
    return render_template("category.html", menu=menu,items=rs, bookmark_list=bookmark_list, bookmark_names=bookmark_names)


@app.route("/detail")
def detail():
    global items, menu
    item_id = 0
    if "id" in request.args:
        item_id = int(request.args["id"])
    item = items[item_id]
    bookmark_names = [x[0] for x in session.get("bookmark_list", [])]
    return render_template("detail.html", item=item, menu=menu, bookmark_list=session.get("bookmark_list", []), bookmark_names=bookmark_names)


@app.route("/auth")
def auth():
    msg = ""
    if "msg" in request.args:
        msg = request.args["msg"]
    return render_template("sign_in.html", error_message=msg)


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
            if os.path.exists(name + ".pickle"):
                with open(name + ".pickle", "rb") as f:
                    bookmark_list = pickle.load(f)
                session["bookmark_list"] = bookmark_list
            return redirect("/")
    return redirect("/sign_in?msg=登入失敗")


@app.route("/logout")
def logout():
    session["user"] = None
    session["bookmark_list"] = None
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/search")
def search():
    global items
    keyword=request.args["keyword"]

    rs=[]
    for item in items:
       # if keyword in item["key"]:
       #     rs.append(item)

        for k in item["key"]:
            k=k.lower()
            keyword = keyword.lower()
            if keyword in k:
                rs.append(item)
                break
    return render_template("search.html",items=rs)
@app.route("/new_user", methods=["GET", "POST"])
def new_user():

    txt_user = request.form["txt_user"]
    txt_pswd = request.form["txt_pswd"]
    with open("user.txt", "a+") as f:
        f.write("%s,%s\n" % (txt_user, txt_pswd))
    return render_template("registercorrect.html")
@app.route("/registercorrect", methods=["GET", "POST"])
def registercorrect():
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


@app.route("/add_bookmark")
def add_bookmark():
    id = request.args["id"]
    link = request.args["link"]
    bookmark_list = []
    if session.get("bookmart_list", []) is not None:
        bookmark_list = session.get("bookmark_list", [])
    bookmark_list.append([id, link])
    session["bookmark_list"] = bookmark_list
    with open(session["user"] + ".pickle","wb") as f:
        pickle.dump(bookmark_list, f)
    return str(session.get("bookmark_list", []))


@app.route("/remove_bookmark")
def remove_bookmark():
    id = request.args["id"]
    bookmark_list = session.get("bookmark_list", [])
    if session.get("bookmart_list", []) is not None:
        bookmart_list = session.get("bookmart_list", [])
    new_bookmark_list = []
    for bookmark in bookmark_list:
        if bookmark[0] != id:
            new_bookmark_list.append(bookmark)
    session["bookmark_list"] = new_bookmark_list
    with open(session["user"] + ".pickle", "wb") as f:
        pickle.dump(new_bookmark_list, f)
    return str(session.get("bookmark_list", []))

app.run(host="127.0.0.1", port=5000, debug=True)
