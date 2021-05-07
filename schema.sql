CREATE TABLE Usertypes (
    id SERIAL PRIMARY KEY,
    usertype_id INTEGER,
    usertype_name TEXT
);
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    usertype INTEGER REFERENCES usertypes
);
CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    coursename TEXT UNIQUE,
    owner_id INTEGER REFERENCES users,
    passgrade INTEGER DEFAULT 70,
    course_intro TEXT DEFAULT 'Kurssin johdanto'
);
CREATE TABLE Participants (
    student_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);
CREATE TABLE Coursematerials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    material_order INTEGER,
    material_title TEXT,
    material_content TEXT
);

INSERT INTO Usertypes (usertype_id,usertype_name) VALUES (1, 'teacher');
INSERT INTO Usertypes (usertype_id,usertype_name) VALUES (2, 'student');