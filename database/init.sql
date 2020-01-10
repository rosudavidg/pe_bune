-- Initializarea bazei de date
CREATE DATABASE pe_bune;

-- Selectarea bazei de date
use pe_bune;

-- Crearea tabelei pentru nivele
CREATE TABLE levels (
    level int,
    experience int NOT NULL,
    PRIMARY KEY (level)
);

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
    PRIMARY KEY (username),
    FOREIGN KEY (level)
        REFERENCES levels(level)
);

-- Crearea tabelei pentru sesiuni
CREATE TABLE sessions (
    username varchar(64) NOT NULL,
    token varchar(256),
    expiration_date datetime NOT NULL,
    PRIMARY KEY (token),
    FOREIGN KEY (username)
        REFERENCES users(username)
        ON DELETE CASCADE
);

-- Crearea tabelei pentru activation token
CREATE TABLE activations (
    email varchar(256) NOT NULL,
    token varchar(64) NOT NULL UNIQUE,
    PRIMARY KEY (email),
    FOREIGN KEY (email)
        REFERENCES users(email)
        ON DELETE CASCADE
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

-- Crearea tabelei pentru log-uri
CREATE TABLE logs (
    id int AUTO_INCREMENT,
    username varchar(64) NOT NULL,
    log_time datetime NOT NULL,
    description varchar(256) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username)
        REFERENCES users(username)
        ON DELETE CASCADE
);

-- Crearea tabelei pentru meciuri
CREATE TABLE games (
    id int AUTO_INCREMENT,
    username varchar(64) NOT NULL,
    finished BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id),
    FOREIGN KEY (username)
        REFERENCES users(username)
        ON DELETE CASCADE
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
    PRIMARY KEY (id),
    FOREIGN KEY (username)
        REFERENCES users(username)
        ON DELETE CASCADE,
    FOREIGN KEY (game_id)
        REFERENCES games(id)
        ON DELETE CASCADE,
    FOREIGN KEY (quiz_id)
        REFERENCES quizzes(id)
        ON DELETE CASCADE
);

-- Adaugarea de nivele
INSERT INTO levels (level, experience) VALUES (0, 0);
INSERT INTO levels (level, experience) VALUES (1, 100);
INSERT INTO levels (level, experience) VALUES (2, 200);
INSERT INTO levels (level, experience) VALUES (3, 500);
INSERT INTO levels (level, experience) VALUES (4, 1000);
INSERT INTO levels (level, experience) VALUES (5, 2000);
INSERT INTO levels (level, experience) VALUES (6, 5000);
INSERT INTO levels (level, experience) VALUES (7, 10000);
INSERT INTO levels (level, experience) VALUES (8, 20000);
INSERT INTO levels (level, experience) VALUES (9, 50000);
INSERT INTO levels (level, experience) VALUES (10, 100000);
