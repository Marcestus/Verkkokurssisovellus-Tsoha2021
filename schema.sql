CREATE TABLE usertypes (
    id SERIAL PRIMARY KEY,
    usertype_id INTEGER,
    usertype_name TEXT
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    usertype INTEGER REFERENCES usertypes
);
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    coursename TEXT UNIQUE,
    owner_id INTEGER REFERENCES users,
    pass_grade INTEGER DEFAULT 70
);
CREATE TABLE participants (
    student_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES courses
);
CREATE TABLE ordervalues (
    id SERIAL PRIMARY KEY,
    ordervalue INTEGER
);
CREATE TABLE coursematerials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    ordervalue INTEGER REFERENCES ordervalues,
    material TEXT
);

INSERT INTO usertypes (usertype_id,usertype_name) VALUES (1, 'opettaja');
INSERT INTO usertypes (usertype_id,usertype_name) VALUES (2, 'opiskelija');
INSERT INTO ordervalues (ordervalue) VALUES (1);
INSERT INTO ordervalues (ordervalue) VALUES (2);
INSERT INTO ordervalues (ordervalue) VALUES (3);
INSERT INTO ordervalues (ordervalue) VALUES (4);
INSERT INTO ordervalues (ordervalue) VALUES (5);
INSERT INTO ordervalues (ordervalue) VALUES (6);
INSERT INTO ordervalues (ordervalue) VALUES (7);
INSERT INTO ordervalues (ordervalue) VALUES (8);
INSERT INTO ordervalues (ordervalue) VALUES (9);
INSERT INTO ordervalues (ordervalue) VALUES (10);
INSERT INTO ordervalues (ordervalue) VALUES (11);
INSERT INTO ordervalues (ordervalue) VALUES (12);
INSERT INTO ordervalues (ordervalue) VALUES (13);