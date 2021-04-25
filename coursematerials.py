from db import db
import courses

def save_material(course_id, coursematerial):
    print(type(coursematerial))
    try:
        sql = "INSERT INTO coursematerials (course_id,material) VALUES(:course_id,:coursematerial)"
        db.session.execute(sql, {"course_id":course_id,"coursematerial":coursematerial})
        db.session.commit()
    except:
        return False
    return True

def get_materials(course_id):
    sql = "SELECT material FROM coursematerials WHERE course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()