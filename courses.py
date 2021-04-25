from db import db
import users

def owned_courses():
    owner_id = users.user_id()
    sql = "SELECT id, coursename FROM courses WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def users_courses():
    user_id = users.user_id()
    sql = "SELECT C.id, C.coursename FROM participants P, courses C WHERE P.student_id=:user_id AND P.course_id=C.id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def all_courses():
    user_id = users.user_id
    sql = "SELECT id, coursename FROM courses"
    result = db.session.execute(sql)
    return result.fetchall()

def open_courses():
    # Voiko tämän suorittaa yhdellä kyselyllä?

    # Haetaan erikseen kaikki kurssit ja kurssit,
    # joille opiskelija on ilmoittautunut
    other_courses = all_courses()
    signedup_courses = users_courses()

    # Käydään läpi kaikki kurssit ja
    # valitaan avoimiin kursseihin vain ne,
    # joihin opiskelija ei ole ilmoittautunut
    open_courses = []
    for course in other_courses:
        if not course in signedup_courses:
            open_courses.append(course)
    
    return open_courses

def get_course(id):
    sql = "SELECT * FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def create_new(coursename):
    owner_id = users.user_id()
    try:
        sql = "INSERT INTO courses (coursename,owner_id) VALUES (:coursename,:owner_id)"
        db.session.execute(sql, {"coursename":coursename,"owner_id":owner_id})
        db.session.commit()
    except:
        return False
    return True

def signup_to_course(course_id):
    user_id = users.user_id()
    try:
        sql = "INSERT INTO participants (student_id, course_id) VALUES (:user_id,:course_id)"
        db.session.execute(sql, {"user_id":user_id,"course_id":course_id})
        db.session.commit()
    except:
        return False
    return True