CREATE TABLE Usertypes (
    id SERIAL PRIMARY KEY,
    usertype_id INTEGER,
    usertype_name TEXT
);
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    usertype INTEGER REFERENCES Usertypes
);
CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    coursename TEXT UNIQUE,
    owner_id INTEGER REFERENCES Users,
    passgrade INTEGER DEFAULT 70,
    course_intro TEXT DEFAULT 'Kurssin johdanto'
);
CREATE TABLE Participants (
    student_id INTEGER REFERENCES users,
    course_id INTEGER REFERENCES Courses,
    course_passed BOOLEAN DEFAULT FALSE
);
CREATE TABLE Coursematerials (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    material_order INTEGER,
    material_title TEXT,
    material_content TEXT
);
CREATE TABLE Exercisetypes (
    id SERIAL PRIMARY KEY,
    exercisetype_id INTEGER,
    exercisetype_name TEXT
);
CREATE TABLE Exercises (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses,
    exercisetype INTEGER REFERENCES Exercisetypes,
    points INTEGER,
    question TEXT NOT NULL,
    right_text TEXT,
    right_feedback TEXT DEFAULT 'Oikein!',
    false_feedback TEXT DEFAULT 'Väärin!'
);
CREATE TABLE Choices (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES Exercises,
    choice TEXT,
    correctness BOOLEAN
);
CREATE TABLE Answers (
    student_id INTEGER REFERENCES Users,
    exercise_id INTEGER REFERENCES Exercises,
    answer_right BOOLEAN
);
CREATE TABLE Done_exercises (
    student_id INTEGER REFERENCES Users,
    course_id INTEGER REFERENCES Courses,
    exercise_type INTEGER REFERENCES Exercisetypes
);

INSERT INTO Usertypes (usertype_id, usertype_name) VALUES (1, 'teacher');
INSERT INTO Usertypes (usertype_id, usertype_name) VALUES (2, 'student');
INSERT INTO Exercisetypes (exercisetype_id, exercisetype_name) VALUES (1, 'quiz');
INSERT INTO Exercisetypes (exercisetype_id, exercisetype_name) VALUES (2, 'text');
