from db import db
import courses

def save_material(course_id, material, material_id):
    try:
        sql = "UPDATE coursematerials SET material=:material WHERE id=:material_id"
        db.session.execute(sql, {"material":material,"material_id":material_id})
        db.session.commit()
    except:
        return False
    return True

def get_materials(course_id):
    sql = "SELECT id, material FROM coursematerials WHERE course_id=:course_id ORDER BY ordervalue"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def initiate_materials(course_id):
    for i in range(1,14):
        if i % 2 != 0:
            text = f"Lisää teksti tähän"
        else:
            text = f"Väliotsikko"
        try:
            sql = "INSERT INTO coursematerials (course_id,ordervalue,material) VALUES(:course_id,:i,:text)"
            db.session.execute(sql, {"course_id":course_id,"i":i,"text":text})
            db.session.commit()
        except:
            return False
    return True