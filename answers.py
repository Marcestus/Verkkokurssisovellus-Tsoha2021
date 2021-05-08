from db import db
import courses


#Täällä vois olla osa sellaisia, että voisi siirtää omaan statistics.py -tiedostoon?

def save_answers(user_id, course_id, exercise_type, answers):
    try:
        for answer in answers:
            if exercise_type == 1:
                answer_as_list = answer.strip(')(').split(', ')
                quiz_id = answer_as_list[1]
                choice_id = answer_as_list[0]
                answer_right = answer_as_list[3]
                sql = "INSERT INTO Answers (student_id, exercise_id, choice_id, answer_right) VALUES (:user_id, :quiz_id, :choice_id, :answer_right)"
                db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id, "choice_id":choice_id, "answer_right":answer_right})
            if exercise_type == 2:
                quiz_id = answer[0]
                text_answer = answer[1]
                answer_right = check_answer(answer)
                sql = "INSERT INTO Answers (student_id, exercise_id, text_answer, answer_right) VALUES (:user_id, :quiz_id, :text_answer, :answer_right)"
                db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id, "text_answer":text_answer, "answer_right":answer_right})
        if not mark_exercises_as_done(user_id, course_id, exercise_type):
            return False
        if not course_already_passed(user_id, course_id) and points_enough_to_pass(user_id, course_id):
            mark_course_as_passed(user_id, course_id)
        db.session.commit()
    except:
        return False
    return True

def check_answer(answer):
    exercise_id = answer[0]
    sql = "SELECT right_text FROM Exercises WHERE id=:exercise_id"
    result = db.session.execute(sql, {"exercise_id":exercise_id})
    right_answer = result.fetchone()[0]
    if answer[1] == right_answer:
        return True
    else:
        return False

def mark_exercises_as_done(user_id, course_id, exercise_type):
    try:
        sql = "INSERT INTO Done_exercises (student_id, course_id, exercise_type) VALUES (:user_id, :course_id, :exercise_type)"
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
    except:
        return False
    return True

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

def get_passgrade_in_points(user_id, course_id):
    return int(get_max_points(course_id)*(get_passgrade(course_id)/100)) + 1

def points_enough_to_pass(user_id, course_id):
    user_points = get_user_points(user_id, course_id)
    max_points = get_max_points(course_id)
    passgrade = get_passgrade(course_id)
    return user_points / max_points >= passgrade / 100

def mark_course_as_passed(user_id, course_id):
    try:
        sql = "UPDATE Participants SET course_passed=TRUE WHERE student_id=:user_id AND course_id=:course_id"
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    except:
        return False
    return True

def all_exercises_answered(user_id, course_id, exercise_type):
    sql = "SELECT 1 FROM Done_exercises WHERE student_id=:user_id AND course_id=:course_id AND exercise_type=:exercise_type"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
    return result.fetchone() != None

def get_correct_answers(user_id, course_id, exercise_type):
    if exercise_type == 1:
        sql = "SELECT exercise_id, choice_id FROM Answers WHERE student_id=:user_id AND answer_right=TRUE AND exercise_id IN (SELECT id FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercise_type)"
    if exercise_type == 2:
        sql = "SELECT exercise_id, text_answer FROM Answers WHERE student_id=:user_id AND answer_right=TRUE AND exercise_id IN (SELECT id FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercise_type)"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
    correct_answers = [(item[0],item[1]) for item in result.fetchall()]
    return correct_answers

def get_all_answers(user_id, course_id, exercise_type):
    if exercise_type == 1:
        sql = "SELECT exercise_id, choice_id FROM Answers WHERE student_id=:user_id AND exercise_id IN (SELECT id FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercise_type)"
    if exercise_type == 2:
        sql = "SELECT exercise_id, text_answer FROM Answers WHERE student_id=:user_id AND exercise_id IN (SELECT id FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercise_type)"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
    all_answers = [(item[0],item[1]) for item in result.fetchall()]
    return all_answers
