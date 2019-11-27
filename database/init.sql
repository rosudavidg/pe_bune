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
    question varchar(256) NOT NULL,
    correct_answer varchar(256) NOT NULL,
    wrong_answer_1 varchar(256) NOT NULL,
    wrong_answer_2 varchar(256) NOT NULL,
    PRIMARY KEY (id)
);

-- Crearea tabelei pentru log-uri

-- Crearea tabelei pentru meciuri