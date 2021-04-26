from app import app
from flask import render_template, request, redirect, session
import users, courses, coursematerials


# Sivuja

@app.route("/")
def index():
    # Suojaus: tehty html-puolella, pitänee siirtää toiminnallisuudet tänne?
    if users.get_usertype() == 1:
        owned_courses = courses.owned_courses()
        return render_template("index.html",owned_courses=owned_courses)
    elif users.get_usertype() == 2:
        users_courses = courses.users_courses()
        open_courses = courses.open_courses()
        return render_template("index.html",users_courses=users_courses,open_courses=open_courses)
    else:
        return render_template("index.html")

@app.route("/course/<int:id>", methods=["get","post"])
def course(id):
    # Suojaus: vain kirjautuneet saa päästä sivuille
    # Suojaus: vain kurssin omistava opettaja saa päästä omistamalleen sivulle
    course = courses.get_course(id)
    if request.method == "GET":
        coursematerial = coursematerials.get_materials(id)
        return render_template("course.html",course=course, coursematerial=coursematerial)
    if request.method == "POST":
        # Tässä ei ole tarkoituksella syötteen rajoitteita kurssimateriaalille (ainakaan vielä)
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if coursematerials.save_material(id, request.form["content"], request.form["material_id"]):
            coursematerial = coursematerials.get_materials(id)
            return render_template("course.html",course=course,coursematerial=coursematerial)
        else:
            return render_template("error.html",message="Kurssimateriaalin tallentaminen ei onnistunut!")

@app.route("/statistics/<int:id>")
def statistics(id):
    # Suojaus: vain käyttäjä itse saa päästä omalle sivulleen
    return render_template("statistics.html",id=id)


#Opettajan toimintoja

@app.route("/newcourse", methods=["post"])
def newcourse():
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    coursename = request.form["coursename"]
    if len(coursename) < 3 or len(coursename) > 100:
        return render_template("error.html",message="Kurssin nimen pituuden täytyy olla 3-100 merkkiä")
    if courses.create_new(coursename):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssin lisääminen ei onnistunut, kurssin nimi saattaa jo olla käytössä...")

@app.route("/addmaterial/<int:id>")
def addmaterial(id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    course = courses.get_course(id)
    materials = coursematerials.get_materials(id)
    return render_template("addmaterial.html",course=course,materials=materials)


# Opiskelijan toimintoja

@app.route("/signup/<int:id>")
def signup(id):
    # Suojaus: vain (kirjautunut) opiskelija voi ilmoittautua kursseille
    if courses.signup_to_course(id):
        return redirect("/")
    else:
        return render_template("error.html",message="Kurssille ilmoittautuminen ei onnistunut")


# Kirjautumiseen liittyvät

@app.route("/login", methods=["post"])
def login():
    # Suojaus: tässä taitaa olla kaikki ihan kunnossa
    # Näissä ei ole CSRF-tsekkausta, ok?
    username = request.form["username"]
    password = request.form["password"]
    if len(username) == 0 or len(password) == 0:
        return render_template("error.html",message="Tunnus tai salasana ei kelpaa, muistithan syöttää molemmat...")
    if users.login(username,password):
        return redirect("/")
    else:
        return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    # Suojaus: tässä taitaa olla kaikki ihan kunnossa
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    # Suojaus: ei tarvetta, kuka vaan voi päästä tänne
    # Näissä ei ole CSRF-tsekkausta, ok?
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usertype = request.form["usertype"]
        if len(username) < 3 or len(username) > 20 or len(password) < 8 or len(password) > 20:
            return render_template("error.html",message="Käyttäjätunnus tai salasana ei kelpaa! Tarkista pituusvaatimukset")
        if users.register(username,password,usertype):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut, tunnus saattaa olla jo käytössä...")