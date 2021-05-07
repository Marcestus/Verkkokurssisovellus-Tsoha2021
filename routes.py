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
    fail = False
    if request.method == "POST":
        # Tässä ei ole tarkoituksella syötteen rajoitteita kurssimateriaalille (ainakaan vielä)
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if request.form["update_type"] == "intro_update":
            if not courses.update_intro(id, request.form["content"]):
                fail = True
        if request.form["update_type"] == "material_update":
            if not coursematerials.update_material(request.form["material_id"], request.form["title"], request.form["content"]):
                fail = True
    if fail:
        return render_template("error.html",message="Kurssimateriaalin päivittäminen ei onnistunut!")
    else:
        course = courses.get_course(id)
        coursematerial = coursematerials.get_materials(id)
        if len(coursematerial) == 0:
            no_material = True
        else:
            no_material = False
        return render_template("course.html",course=course,coursematerial=coursematerial,no_material=no_material)

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

@app.route("/update_passgrade", methods=["post"])
def update_passgrade():
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    new_passgrade = request.form["passgrade"]
    #if new_passgrade < 1 or new_passgrade > 100:
    #    return render_template("error.html",message="Läpipääsyrajan pitää olla välillä 1-100")
    course_id = request.form["course_id"]
    if courses.update_passgrade(course_id, new_passgrade):
        return redirect(f"course/{course_id}")
    else:
        return render_template("error.html",message="Läpipääsyrajan päivittäminen ei onnistunut!")

@app.route("/update_material/<int:course_id>/<int:material_id>")
def update_material(course_id,material_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    course = courses.get_course(course_id)
    material = coursematerials.get_material(material_id)
    return render_template("updatematerial.html",course=course,material=material)

@app.route("/add_material/<int:course_id>/<int:material_id>")
def add_material(course_id,material_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    slotcount = coursematerials.get_amount_of_material_slots(course_id)
    if slotcount >= 10:
        return render_template("error.html",message="Et voi lisätä uusia osioita, maksimimäärä on 10!")
    if coursematerials.add_material(course_id, material_id):
        return redirect(f"/course/{course_id}")
    else:
        return render_template("error.html",message="Materiaalin lisääminen ei onnistunut")

@app.route("/delete_material/<int:course_id>/<int:material_id>")
def delete_material(course_id,material_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    if coursematerials.delete_material(course_id,material_id):
        return redirect(f"/course/{course_id}")
    else:
        return render_template("error.html",message="Materiaalin poistaminen ei onnistunut!")

@app.route("/update_intro/<int:course_id>")
def update_intro(course_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    course = courses.get_course(course_id)
    return render_template("updateintro.html",course=course)

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
        password_again = request.form["password_again"]
        if password != password_again:
            return render_template("error.html",message="Salasanat eivät täsmää, koita uudestaan!")
        if len(username) < 3 or len(username) > 20 or len(password) < 8 or len(password) > 20:
            return render_template("error.html",message="Käyttäjätunnus tai salasana ei kelpaa! Tarkista pituusvaatimukset")
        if users.register(username,password,usertype):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut, tunnus saattaa olla jo käytössä...")