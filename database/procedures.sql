-- Selectarea bazei de date
use pe_bune;

-- Procedura de adaugare a unui user nou
DELIMITER //
CREATE PROCEDURE create_new_user (
    IN username varchar(64),
    IN password varchar(256),
    IN email varchar(256),
    IN first_name varchar(256),
    IN last_name varchar(256))
BEGIN
    INSERT
        INTO users
        VALUES (
            username,
            password,
            email,
            first_name,
            last_name,
            0,
            0,
            sysdate());
END //
DELIMITER ;
