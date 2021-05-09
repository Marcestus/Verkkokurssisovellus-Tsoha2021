from app import app
from flask import render_template, request, redirect, session
import users, courses, coursematerials, exercises, answers, statistics


# Sivuja

@app.route("/")
def index():
    # Suojaus: tehty html-puolella, pitänee siirtää toiminnallisuudet tänne?
    if users.get_usertype() == 1:
        open_courses_teacher = courses.get_open_courses_teacher()
        unpublished_courses = courses.get_unpublished_courses()
        course_statistics = []
        for course in open_courses_teacher:
            student_amount = statistics.get_students(course[0])
            passed_students = statistics.get_passed_students(course[0])
            if student_amount == 0:
                pass_percent = 0
            else:
                pass_percent = int((passed_students / student_amount) * 100)
            course_stats = (course[0], [student_amount, passed_students, pass_percent])
            course_statistics.append(course_stats)
        return render_template("index.html", open_courses_teacher=open_courses_teacher, unpublished_courses=unpublished_courses, course_statistics=course_statistics)
    elif users.get_usertype() == 2:
        completed_courses = courses.get_completed_courses()
        uncompleted_courses = courses.get_uncompleted_courses()
        open_courses = courses.get_open_courses()
        return render_template("index.html", completed_courses=completed_courses, uncompleted_courses=uncompleted_courses, open_courses=open_courses)
    else:
        return render_template("index.html")

@app.route("/course/<int:id>", methods=["get", "post"])
def course_page(id):
    # Suojaus: vain kirjautuneet saa päästä sivuille
    # Suojaus: vain kurssin omistava opettaja saa päästä omistamalleen (muokkaus)sivulle
    fail = False
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        update_type = request.form["update_type"]
        if update_type == "intro_update":
            if not courses.update_intro(id, request.form["content"]):
                fail = True
        if update_type == "material_update":
            if not coursematerials.update_material(request.form["material_id"], request.form["title"], request.form["content"]):
                fail = True
    if fail:
        return render_template("error.html", message="Kurssimateriaalin päivittäminen ei onnistunut!")
    else:
        user_id = users.get_user_id()
        course = courses.get_course(id)
        course_published = course[5]
        coursematerial = coursematerials.get_all_coursematerials(id)
        course_statistics = statistics.get_course_status(user_id, id)
        no_material = (len(coursematerial) == 0)
        no_more_material = (coursematerials.get_amount_of_material_slots(id) == 10)
        return render_template("course.html", course=course, course_published=course_published, coursematerial=coursematerial, course_statistics=course_statistics,
            no_material=no_material, no_more_material=no_more_material)

@app.route("/course/<int:id>/exercises", methods=["get", "post"])
def exercise_page(id):
    # Suojaus: vain kirjautuneet saa päästä sivuille
    # Suojaus: vain kyseiselle kurssille ilmoittautuneet oppilaat pääsee vastaamaan tehtäviin
    # Suojaus: vain kurssin omistava opettaja saa päästä omistamalleen (muokkaus)sivulle
    fail = False
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        exercise_type = int(request.form["exercise_type"])
        if exercise_type == 1:
            right_choice = request.form["right_choice"]
            wrong_choices = request.form.getlist("wrong_choice")
            if not exercises.add_quiz_exercise(id, exercise_type, int(request.form["points"]), request.form["question"],
                request.form["right_feedback"], request.form["false_feedback"], right_choice, wrong_choices):
                fail = True
        if exercise_type == 2:
            if not exercises.add_text_exercise(id, exercise_type, int(request.form["points"]), request.form["question"],
                request.form["right_text"], request.form["right_feedback"], request.form["false_feedback"]):
                fail = True
    if fail:
        return render_template("error.html", message="Tehtävän lisääminen epäonnistui!")
    else:
        user_id = users.get_user_id()
        
        course = courses.get_course(id)
        quiz_exercises = exercises.get_all_quiz_exercises(id)
        quizzes_and_choises = []
        for quiz in quiz_exercises:
            choices = exercises.get_all_choises(quiz[0])
            quizzes_and_choises.append((quiz, choices))
        text_exercises = exercises.get_all_text_exercises(id)

        no_quizzes = (len(quizzes_and_choises) == 0)
        no_text_exercises = (len(text_exercises) == 0)
        all_exercise_slots_used = (exercises.get_amount_of_exercises(id) == 20)
        course_published = course[5]
        student_signedup = courses.check_for_signup(user_id, id)

        all_quizzes_answered = statistics.all_exercises_answered(user_id, id, 1)
        all_text_exercises_answered = statistics.all_exercises_answered(user_id, id, 2)
        
        course_statistics = statistics.get_course_status(user_id, id)

        correct_quiz_answers = []
        correct_text_exercise_answers = []
        all_quiz_answers = []
        all_text_exercise_answers = []
        if all_quizzes_answered:
            correct_quiz_answers = answers.get_correct_answers(user_id, id, 1)
            all_quiz_answers = answers.get_all_answers(user_id, id, 1)
        if all_text_exercises_answered:
            all_text_exercise_answers = answers.get_all_answers(user_id, id, 2)
        
        return render_template("exercises.html",
            course=course, quizzes_and_choises=quizzes_and_choises, text_exercises=text_exercises,
            no_quizzes=no_quizzes, no_text_exercises=no_text_exercises, all_exercise_slots_used=all_exercise_slots_used,
            course_published=course_published, student_signedup=student_signedup,
            all_quizzes_answered=all_quizzes_answered, all_text_exercises_answered=all_text_exercises_answered,
            course_statistics=course_statistics, correct_quiz_answers=correct_quiz_answers,
            all_quiz_answers=all_quiz_answers, all_text_exercise_answers=all_text_exercise_answers)


#Opettajan toimintoja

@app.route("/newcourse", methods=["post"])
def newcourse():
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    coursename = request.form["coursename"]
    if courses.create_new(coursename):
        return redirect("/")
    else:
        return render_template("error.html", message="Kurssin lisääminen ei onnistunut, kurssin nimi saattaa jo olla käytössä...")

@app.route("/update_passgrade", methods=["post"])
def update_passgrade():
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    new_passgrade = request.form["passgrade"]
    course_id = request.form["course_id"]
    if courses.update_passgrade(course_id, new_passgrade):
        return redirect(f"course/{course_id}")
    else:
        return render_template("error.html", message="Läpipääsyrajan päivittäminen ei onnistunut!")

@app.route("/update_intro/<int:course_id>")
def update_intro(course_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    course = courses.get_course(course_id)
    return render_template("updateintro.html", course=course)

@app.route("/update_material/<int:course_id>/<int:material_id>")
def update_material(course_id, material_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    course = courses.get_course(course_id)
    material = coursematerials.get_material(material_id)
    return render_template("updatematerial.html", course=course, material=material)

@app.route("/modify_coursematerial_order/<int:course_id>/<int:material_id>/<string:modify_type>")
def modify_coursematerial_order(course_id, material_id, modify_type):
    # Suojaus: vain (kirjautunut) opettaja saa päästä tänne
    slotcount = coursematerials.get_amount_of_material_slots(course_id)
    if modify_type != "delete" and slotcount >= 10:
        return render_template("error.html", message="Et voi lisätä uusia osioita, maksimimäärä on 10!")
    if coursematerials.modify_material_order(course_id, material_id, modify_type):
        return redirect(f"/course/{course_id}")
    else:
        return render_template("error.html", message="Materiaalin lisääminen ei onnistunut!")

@app.route("/hide/<int:course_id>/<int:exercise_id>")
def hide_exercise(course_id, exercise_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    exercises.hide_exercise(exercise_id)
    return redirect(f"/course/{course_id}/exercises")

@app.route("/publish/<int:course_id>")
def publish_course(course_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    courses.publish_course(course_id)
    return redirect("/")

@app.route("/hide/<int:course_id>")
def hide_course(course_id):
    # Suojaus: vain (kirjautunut) opettaja saa päästä oman kurssinsa muokkaussivulle
    courses.hide_course(course_id)
    return redirect("/")


# Opiskelijan toimintoja

@app.route("/signup/<int:id>")
def signup(id):
    # Suojaus: vain (kirjautunut) opiskelija voi ilmoittautua kursseille
    if courses.signup_to_course(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Kurssille ilmoittautuminen ei onnistunut")

@app.route("/answer_to_exercises", methods=["post"])
def answer_to_exercises():
    # Suojaus: vain kyseiselle kurssille ilmoittautunut (kirjautunut) opiskelija
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    user_id = users.get_user_id()
    course_id = request.form["course_id"]
    exercise_type = int(request.form["exercise_type"])

    all_answers = []
    if exercise_type == 1:
        all_quizzes = request.form.getlist("quizzes")
        for exercise_id in all_quizzes:
            all_answers.append(request.form[f"choice_{exercise_id}"])
    if exercise_type == 2:
        all_text_exercises = request.form.getlist("texts")
        for exercise_id in all_text_exercises:
            all_answers.append((exercise_id, request.form[f"answer_{exercise_id}"]))
    
    if answers.save_answers(user_id, course_id, exercise_type, all_answers):
        return redirect(f"/course/{course_id}/exercises")
    else:
        return render_template("error.html", message="Vastausten tallentaminen ei onnistunut!")


# Kirjautumiseen liittyvät

@app.route("/login", methods=["get", "post"])
def login():
    # Suojaus: tässä taitaa olla kaikki ihan kunnossa
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    # Suojaus: tässä taitaa olla kaikki ihan kunnossa
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    # Suojaus: ei tarvetta, kuka vaan voi päästä tänne
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usertype = request.form["usertype"]
        password_again = request.form["password_again"]
        if password != password_again:
            return render_template("error.html", message="Salasanat eivät täsmää, koita uudestaan!")
        if users.register(username, password, usertype):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut, tunnus saattaa olla jo käytössä...")