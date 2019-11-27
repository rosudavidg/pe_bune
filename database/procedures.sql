-- Selectarea bazei de date
use pe_bune;

-- Procedura de adaugare a unui user nou
DELIMITER //
CREATE PROCEDURE create_user (
    IN username varchar(64),
    IN password varchar(256),
    IN email varchar(256),
    IN first_name varchar(256),
    IN last_name varchar(256),
    IN token varchar(64))
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
            sysdate(),
            False
        );
    INSERT
        INTO activations
        VALUES (
            email,
            token
        );
    COMMIT;
END //
DELIMITER ;

-- Procedura de activare a unui utilizator
DELIMITER //
CREATE PROCEDURE confirm_user (
    IN token varchar(64),
    OUT out_ans boolean)
BEGIN

    SELECT activation_token_exists(token) INTO out_ans;

    IF out_ans = TRUE THEN
        DELETE
            FROM activations a
            WHERE a.token = token
        ;
        COMMIT;
    END IF;
    
END //
DELIMITER ;

-- Procedura primeste email-ul si paseaza inapoi token-ul
DELIMITER //
CREATE PROCEDURE get_activation_token (
    IN in_email varchar(256),
    OUT out_token varchar(64))
BEGIN
    SELECT
        token INTO out_token
        FROM activations
        WHERE email = in_email
    ;
END //
DELIMITER ;
