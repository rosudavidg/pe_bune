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
    PRIMARY KEY (username)
);

-- Crearea tabelei pentru sesiuni

-- Crearea tabelei pentru intrebari

-- Crearea tabelei pentru raspunsuri

-- Crearea tabelei pentru log-uri

-- Crearea tabelei pentru meciuri