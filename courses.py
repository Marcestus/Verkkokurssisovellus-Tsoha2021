from db import db
import users, coursematerials

def owned_courses():
    owner_id = users.user_id()
    sql = "SELECT id, coursename FROM Courses WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def users_courses():
    user_id = users.user_id()
    sql = "SELECT C.id, C.coursename FROM Participants P, courses C WHERE P.student_id=:user_id AND P.course_id=C.id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def all_courses():
    user_id = users.user_id
    sql = "SELECT id, coursename FROM Courses"
    result = db.session.execute(sql)
    return result.fetchall()

def open_courses():
    # Voikohan tämän suorittaa yhdellä SQL-kyselyllä?
    other_courses = all_courses()
    signedup_courses = users_courses()
    open_courses = []
    for course in other_courses:
        if not course in signedup_courses:
            open_courses.append(course)
    return open_courses

def get_course(id):
    sql = "SELECT * FROM Courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_course_id(coursename):
    sql = "SELECT id FROM Courses WHERE coursename=:coursename"
    result = db.session.execute(sql, {"coursename":coursename})
    course_id = result.fetchone()
    return course_id[0]

def create_new(coursename):
    owner_id = users.user_id()
    try:
        create_course = "INSERT INTO Courses (coursename,owner_id) VALUES (:coursename,:owner_id)"
        db.session.execute(create_course, {"coursename":coursename,"owner_id":owner_id})
        db.session.commit()
    except:
        return False
    return True

def update_passgrade(course_id,passgrade):
    try:
        sql = "UPDATE Courses SET passgrade=:passgrade WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id,"passgrade":passgrade})
        db.session.commit()
    except:
        return False
    return True

def update_intro(course_id,intro):
    try:
        sql = "UPDATE Courses SET course_intro=:intro WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id,"intro":intro})
        db.session.commit()
    except:
        return False
    return True


def signup_to_course(course_id):
    user_id = users.user_id()
    try:
        sql = "INSERT INTO Participants (student_id, course_id) VALUES (:user_id,:course_id)"
        db.session.execute(sql, {"user_id":user_id,"course_id":course_id})
        db.session.commit()
    except:
        return False
    return True