from db import db

def course_already_passed(user_id, course_id):
    sql = "SELECT 1 FROM Participants WHERE student_id=:user_id AND course_id=:course_id AND course_passed=TRUE"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    return result.fetchone() != None

def get_max_points(course_id):
    sql = "SELECT SUM(points) FROM Exercises WHERE course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]

def get_user_points(user_id, course_id):
    sql = "SELECT SUM(points) FROM Exercises WHERE course_id=:course_id AND id IN (SELECT exercise_id FROM Answers WHERE student_id=:user_id AND answer_right=TRUE)"
    result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    return result.fetchone()[0]

def get_passgrade(course_id):
    sql = "SELECT passgrade FROM Courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]

def get_passgrade_in_points(course_id):
    return 1 #int(get_max_points(course_id))*int((get_passgrade(course_id)/100)) + 1

def points_enough_to_pass(user_id, course_id):
    user_points = get_user_points(user_id, course_id)
    max_points = get_max_points(course_id)
    passgrade = get_passgrade(course_id)
    return user_points / max_points >= passgrade / 100

def all_exercises_answered(user_id, course_id, exercise_type):
    sql = "SELECT 1 FROM Done_exercises WHERE student_id=:user_id AND course_id=:course_id AND exercise_type=:exercise_type"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
    return result.fetchone() != None

def exercises_completed(user_id, course_id):
    return all_exercises_answered(user_id, course_id, 1) and all_exercises_answered(user_id, course_id, 2)

def get_course_status(user_id, course_id):
    course_statistics = []
    course_statistics.append(get_max_points(course_id))
    course_statistics.append(get_user_points(user_id, course_id))
    course_statistics.append(get_passgrade(course_id))
    course_statistics.append(get_passgrade_in_points(course_id))
    if course_already_passed(user_id, course_id):
        course_statistics.append("Suoritettu hyväksytysti")
    elif exercises_completed(user_id, course_id):
        course_statistics.append("Hylätty")
    else:
        course_statistics.append("Kesken")
    return course_statistics