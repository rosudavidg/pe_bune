-- Initializarea bazei de date
CREATE DATABASE pe_bune;

-- Selectarea bazei de date
use pe_bune;

-- Crearea tabelei pentru utilizatori
CREATE TABLE users (
    username varchar(64),
    password varchar(256) NOT NULL,
    email varchar(256) NOT NULL UNIQUE,
    first_name varchar(256) NOT NULL,
    last_name varchar(256) NOT NULL,
    level int NOT NULL,
    experience int NOT NULL,
    created_date datetime NOT NULL,
    activated BOOLEAN NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (username)
);

-- Crearea tabelei pentru sesiuni
CREATE TABLE sessions (
    username varchar(64) NOT NULL,
    token varchar(256),
    expiration_date datetime NOT NULL,
    PRIMARY KEY (token)
);

-- Crearea tabelei pentru activation token
CREATE TABLE activations (
    email varchar(256) NOT NULL,
    token varchar(64),
    PRIMARY KEY (email)
);

-- Crearea tabelei pentru intrebari
CREATE TABLE quizzes (
    id int AUTO_INCREMENT,
    category varchar(256) NOT NULL,
    question varchar(256) NOT NULL,
    correct_answer varchar(256) NOT NULL,
    wrong_answer_1 varchar(256) NOT NULL,
    wrong_answer_2 varchar(256) NOT NULL,
    PRIMARY KEY (id)
);

-- TODO: Crearea tabelei pentru log-uri

-- Crearea tabelei pentru meciuri
CREATE TABLE games (
    id int AUTO_INCREMENT,
    username varchar(64) NOT NULL,
    finished BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id)
);

-- Crearea tabelei pentru intrebarile asociate jocurilor
CREATE TABLE games_quizzes (
    id int AUTO_INCREMENT,
    game_id int NOT NULL,
    username varchar(64) NOT NULL,
    quiz_id int NOT NULL,
    answered BOOLEAN NOT NULL DEFAULT FALSE,
    correct BOOLEAN NOT NULL DEFAULT FALSE,
    time int NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

-- Crearea tabelei pentru nivele
CREATE TABLE levels (
    level int,
    experience int NOT NULL,
    PRIMARY KEY (level)
);

-- Adaugarea de nivele
INSERT INTO levels (level, experience) VALUES (1, 10);
INSERT INTO levels (level, experience) VALUES (2, 20);
INSERT INTO levels (level, experience) VALUES (3, 50);
INSERT INTO levels (level, experience) VALUES (4, 100);
INSERT INTO levels (level, experience) VALUES (5, 200);
INSERT INTO levels (level, experience) VALUES (6, 500);
INSERT INTO levels (level, experience) VALUES (7, 1000);
INSERT INTO levels (level, experience) VALUES (8, 2000);
INSERT INTO levels (level, experience) VALUES (9, 5000);
INSERT INTO levels (level, experience) VALUES (10, 10000);
