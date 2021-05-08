from db import db
import random
import courses

def update_exercise():
    # jos joku on jo ratkonut tehtävän, sitä ei voi enää päivittää
    print("Sukka")

def delete_exercise():
    # jos joku on jo ratkonut tehtävän, sitä ei voi enää poistaa
    print("Sukka")

def add_quiz_exercise(course_id, exercisetype, points, question, right_feedback, false_feedback, right_choice, wrong_choices):
    try:
        sql = "INSERT INTO Exercises (course_id, exercisetype, points, question, right_text, right_feedback, false_feedback) VALUES (:course_id, :exercisetype, :points, :question, 'testi', :right_feedback, :false_feedback) RETURNING id"
        result = db.session.execute(sql, {"course_id":course_id, "exercisetype":exercisetype, "points":points, "question":question, "right_feedback":right_feedback, "false_feedback":false_feedback})
        exercise_id = result.fetchone()[0]
        sql = "INSERT INTO Choices (exercise_id, choice, correctness) VALUES (:exercise_id, :right_choice, TRUE)"
        db.session.execute(sql, {"exercise_id":exercise_id, "right_choice":right_choice})
        for choice in wrong_choices:
            if len(choice) != 0:
                sql = "INSERT INTO Choices (exercise_id, choice, correctness) VALUES (:exercise_id, :choice, FALSE)"
                db.session.execute(sql, {"exercise_id":exercise_id, "choice":choice})
        db.session.commit()
    except:
        return False
    return True

def add_text_exercise(course_id, exercisetype, points, question, right_text, right_feedback, false_feedback):
    try:
        sql = "INSERT INTO Exercises (course_id, exercisetype, points, question, right_text, right_feedback, false_feedback) VALUES (:course_id, :exercisetype, :points, :question, :right_text, :right_feedback, :false_feedback)"
        db.session.execute(sql, {"course_id":course_id, "exercisetype":exercisetype, "points":points, "question":question, "right_text":right_text, "right_feedback":right_feedback, "false_feedback":false_feedback})
        db.session.commit()
    except:
        return False
    return True

def get_all_quiz_exercises(course_id):
    exercisetype = 1
    sql = "SELECT id, points, question, right_feedback, false_feedback FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercisetype"
    result = db.session.execute(sql, {"course_id":course_id, "exercisetype":exercisetype})
    random_order = result.fetchall()
    return random.sample(random_order, len(random_order))

def get_all_choises(quiz_id):
    sql = "SELECT id, exercise_id, choice, correctness FROM Choices WHERE exercise_id=:quiz_id"
    result = db.session.execute(sql, {"quiz_id":quiz_id})
    random_order = result.fetchall()
    return random.sample(random_order, len(random_order))

def get_all_text_exercises(course_id):
    exercisetype = 2
    sql = "SELECT id, points, question, right_text, right_feedback, false_feedback FROM Exercises WHERE course_id=:course_id AND exercisetype=:exercisetype"
    result = db.session.execute(sql, {"course_id":course_id, "exercisetype":exercisetype})
    random_order = result.fetchall()
    return random.sample(random_order, len(random_order))

def get_amount_of_exercises(course_id):
    sql = "SELECT COUNT(*) FROM Exercises WHERE course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchone()[0]
