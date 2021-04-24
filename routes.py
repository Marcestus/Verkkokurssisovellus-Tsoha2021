from app import app
from flask import render_template, request, redirect
import users, courses

@app.route("/")
def index():

    if users.get_usertype() == 0:
        users_courses = courses.users_courses()
        open_courses = courses.open_courses()
        return render_template("index.html",users_courses=users_courses,open_courses=open_courses)
    elif users.get_usertype() == 1:
        owned_courses = courses.owned_courses()
        return render_template("index.html",owned_courses=owned_courses)
    
    return render_template("index.html")

@app.route("/newcourse", methods=["post"])
def newcourse():
    coursename = request.form["coursename"]
    if courses.create_new(coursename):
        return redirect("/")
    else:
        return render_template("error.html", message="Kurssin lisääminen ei onnistunut")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/login", methods=["post"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
        return redirect("/")
    else:
        return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usertype = request.form["usertype"]
        if users.register(username,password,usertype):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")