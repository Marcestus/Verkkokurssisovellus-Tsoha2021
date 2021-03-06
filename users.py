import os
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id, usertype FROM Users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["username"] = username
            session["usertype"] = user[2]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["usertype"]

def register(username, password, usertype):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username, password, usertype) VALUES (:username, :password, :usertype)"
        db.session.execute(sql, {"username":username, "password":hash_value, "usertype":usertype})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_user_id():
    return session.get("user_id", 0)

def get_usertype():
    return session.get("usertype")