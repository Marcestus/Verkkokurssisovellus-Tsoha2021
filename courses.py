from db import db
import users, coursematerials, statistics

def get_open_courses_teacher():
    owner_id = users.get_user_id()
    sql = "SELECT id, coursename FROM Courses WHERE owner_id=:owner_id AND published=TRUE AND visible=TRUE"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def get_unpublished_courses():
    owner_id = users.get_user_id()
    sql = "SELECT id, coursename FROM Courses WHERE owner_id=:owner_id AND published=FALSE AND visible=TRUE"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def hide_course(course_id):
    try:
        sql = "UPDATE Courses SET visible=FALSE WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id})
        db.session.commit()
    except:
        return False
    return True

def publish_course(course_id):
    try:
        sql = "UPDATE Courses SET published=TRUE WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id})
        db.session.commit()
    except:
        return False
    return True

def get_all_users_courses():
    user_id = users.get_user_id()
    sql = "SELECT C.id, C.coursename FROM Participants P, courses C WHERE P.student_id=:user_id AND P.course_id=C.id AND C.published=TRUE AND C.visible=TRUE"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_completed_courses():
    all_courses = get_all_users_courses()
    user_id = users.get_user_id()
    completed_courses = []
    for course in all_courses:
        if statistics.exercises_completed(user_id, course[0]):
            completed_courses.append(course)
    return completed_courses

def get_uncompleted_courses():
    all_courses = get_all_users_courses()
    user_id = users.get_user_id()
    uncompleted_courses = []
    for course in all_courses:
        if not statistics.exercises_completed(user_id, course[0]):
            uncompleted_courses.append(course)
    return uncompleted_courses

def get_all_published_courses():
    sql = "SELECT id, coursename FROM Courses WHERE published=TRUE AND visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def get_open_courses():
    other_courses = get_all_published_courses()
    signedup_courses = get_all_users_courses()
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
    owner_id = users.get_user_id()
    try:
        sql = "INSERT INTO Courses (coursename, owner_id) VALUES (:coursename, :owner_id)"
        db.session.execute(sql, {"coursename":coursename, "owner_id":owner_id})
        db.session.commit()
    except:
        return False
    return True

def update_passgrade(course_id, passgrade):
    try:
        sql = "UPDATE Courses SET passgrade=:passgrade WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id, "passgrade":passgrade})
        db.session.commit()
    except:
        return False
    return True

def update_intro(course_id, intro):
    try:
        sql = "UPDATE Courses SET course_intro=:intro WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id, "intro":intro})
        db.session.commit()
    except:
        return False
    return True

def signup_to_course(course_id):
    user_id = users.get_user_id()
    try:
        sql = "INSERT INTO Participants (student_id, course_id) VALUES (:user_id, :course_id)"
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
        db.session.commit()
    except:
        return False
    return True

def check_for_signup(user_id, course_id):
    sql = "SELECT 1 FROM Participants WHERE student_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    return result.fetchone() != None

def check_for_ownership(user_id, course_id):
    sql = "SELECT 1 FROM Courses WHERE owner_id=:user_id AND id=:course_id"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    return result.fetchone() != None