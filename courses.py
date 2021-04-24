from db import db
import users

def owned_courses():
    owner_id = users.user_id()
    sql = "SELECT coursename FROM courses WHERE owner_id=:owner_id"
    result = db.session.execute(sql, {"owner_id":owner_id})
    return result.fetchall()

def users_courses():
    user_id = users.user_id()
    sql = "SELECT C.coursename FROM participants P, courses C WHERE P.student_id=:user_id AND P.course_id=C.id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def open_courses():
    sql = "SELECT coursename FROM courses"
    result = db.session.execute(sql)
    return result.fetchall()

def create_new(coursename):
    owner_id = users.user_id()
    passgrade = 70
    try:
        sql = "INSERT INTO courses (coursename,owner_id,pass_grade) VALUES (:coursename,:owner_id,:passgrade)"
        db.session.execute(sql, {"coursename":coursename,"owner_id":owner_id,"passgrade":passgrade})
        db.session.commit()
    except:
        return False
    return True
    