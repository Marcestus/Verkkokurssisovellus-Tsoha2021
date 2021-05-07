from db import db
import courses

def get_material(material_id):
    sql = "SELECT id, material_title, material_content FROM Coursematerials WHERE id=:material_id"
    result = db.session.execute(sql, {"material_id":material_id})
    return result.fetchone()

def get_materials(course_id):
    sql = "SELECT id, material_title, material_content FROM Coursematerials WHERE course_id=:course_id ORDER BY material_order"
    result = db.session.execute(sql, {"course_id":course_id})
    return result.fetchall()

def get_amount_of_material_slots(course_id):
    sql = "SELECT COUNT(*) FROM Coursematerials WHERE course_id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    amount = result.fetchone()
    return amount[0]

def get_ordervalue(material_id):
    sql = "SELECT material_order FROM Coursematerials WHERE id=:material_id"
    result = db.session.execute(sql, {"material_id":material_id})
    ordervalue = result.fetchone()
    return ordervalue[0]

def add_material(course_id, material_id):
    if material_id == 0:
        ordervalue = 1
    else:
        ordervalue = get_ordervalue(material_id) + 1
    if update_ordervalues(course_id, material_id, "add"):
        title = "Väliotsikko"
        text = "Lisää materiaali tähän"
        try:
            sql = "INSERT INTO Coursematerials (course_id, material_order, material_title, material_content) VALUES (:course_id,:ordervalue,:title,:text)"
            db.session.execute(sql, {"course_id":course_id,"ordervalue":ordervalue,"title":title,"text":text})
            db.session.commit()
        except:
            return False
        return True
    else:
        return False

def delete_material(course_id, material_id):
    if update_ordervalues(course_id, material_id, "delete"):
        try:
            sql = "DELETE FROM Coursematerials WHERE id=:material_id"
            db.session.execute(sql, {"material_id":material_id})
            db.session.commit()
        except:
            return False
        return True
    else:
        return False
    
def update_ordervalues(course_id, material_id, update_type):
    if material_id == 0:
        return True
    if update_type == "delete":
        change = -1
        interval = 1
        first = get_ordervalue(material_id) + 1
        last = get_amount_of_material_slots(course_id) + 1
    if update_type == "add":
        change = 1
        interval = -1
        first = get_amount_of_material_slots(course_id)
        last = get_ordervalue(material_id)
    for i in range(first,last,interval):
        try:
            sql = "UPDATE Coursematerials SET material_order=material_order+:change WHERE course_id=:course_id AND material_order=:i"
            db.session.execute(sql, {"course_id":course_id,"change":change,"i":i})
        except:
            return False
    return True

def update_material(material_id,title,text):
    try:
        sql = "UPDATE Coursematerials SET material_title=:title, material_content=:text WHERE id=:material_id"
        db.session.execute(sql, {"material_id":material_id,"title":title,"text":text})
        db.session.commit()
    except:
        return False
    return True


