from db import db
import courses

def save_answers(exercise_type, user_id, answers, course_id):
    try:
        for answer in answers:
            if exercise_type == 1:
                answer_as_list = answer.strip(')(').split(', ')
                quiz_id = answer_as_list[1]
                answer_right = answer_as_list[3]
            if exercise_type == 2:
                quiz_id = answer[0]
                answer_right = check_answer(answer)
            sql = "INSERT INTO Answers (student_id, exercise_id, answer_right) VALUES (:user_id, :quiz_id, :answer_right)"
            db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id, "answer_right":answer_right})
        if not mark_exercises_done(user_id, course_id, exercise_type):
            return False
        if course_passed(user_id, course_id):
            mark_course_passed(user_id, course_id)
        db.session.commit()
    except:
        return False
    return True

def count_right_answers(student_id, course_id, exercise_type):
    #Tää ehkä sopii paremmin tilastoihin
    print("sukka")

def mark_exercises_done(user_id, course_id, exercise_type):
    try:
        sql = "INSERT INTO Done_exercises (student_id, course_id, exercise_type) VALUES (:user_id, :course_id, :exercise_type)"
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id, "exercise_type":exercise_type})
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



def course_passed(user_id, course_id):
    return False
    #tarvitaan tehtävät ja vastaukset
    #eli pitää verrata kurssin tehtävien kokonaispisteitä
    #opiskelijan keräämiin pisteisiin ja katsoa,
    #onko kerättyjen pisteiden prosenttiosuus kokonaispisteistä
    #yli kurssin läpipääsyrajan

    #huomioi, että jos on jo passed niin ei tarvi tehdä mitään