CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, usertype INTEGER);
CREATE TABLE courses (id SERIAL PRIMARY KEY, coursename TEXT UNIQUE, owner_id INTEGER, pass_grade INTEGER);
CREATE TABLE participants (student_id INTEGER, course_id INTEGER);