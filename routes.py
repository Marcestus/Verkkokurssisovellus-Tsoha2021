from app import app
from flask import render_template, request, redirect
import users, courses

@app.route("/")
def index():

    # Tarviiko tässä huomioida kirjautumista muuten kuin index näyttää session-tietojen mukaan eri näkymän?

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

    # Tääkin pitää varmaan suojata niin, että vain (kirjautuneet) opet pääsee tähän sivulle

    coursename = request.form["coursename"]
    if courses.create_new(coursename):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin lisääminen ei onnistunut")

@app.route("/course/<int:id>")
def course(id):

    # Tänne pitää nyt ainakin laittaa se,
    # että jos on opettajaroolissa niin ei pääse kuin omalle sivulleen
    # Eli jos usertype on ope, owner_id pitää olla user_id ennen kun näkee sivun

    # Ja tähän myös, että jos ei oo kirjautunut, niin ei näe sivua

    course = courses.get_course(id)
    return render_template("course.html",course=course)

@app.route("/signup/<int:id>")
def signup(id):

    # Tännekään ei taida tarvita päästä kuin kirjautuneet

    if courses.signup_to_course(id):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssille ilmoittautuminen ei onnistunut")

@app.route("/statistics")
def statistics():

    # Täällä pitää varmistaa, että jokainen näkee vain omat tietonsa
    # Eikä pääse kirjautumatta sivulle

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