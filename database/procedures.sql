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

-- Procedura primeste username-ul si paseaza inapoi parola criptata
DELIMITER //
CREATE PROCEDURE get_password (
    IN in_username varchar(64),
    OUT out_password varchar(256))
BEGIN
    SELECT
        password INTO out_password
        FROM users
        WHERE username = in_username
    ;
END //
DELIMITER ;

-- Procedura primeste username-ul si intoarce daca contul este activat sau nu
DELIMITER //
CREATE PROCEDURE is_active (
    IN in_username varchar(64),
    OUT out_active boolean)
BEGIN
    DECLARE counter integer;

    SELECT
        COUNT(*) INTO counter
        FROM users
        WHERE username = in_username
        AND activated = TRUE
    ;

    IF counter = 1 THEN
        SET out_active = TRUE;
    ELSE
        SET out_active = FALSE;
    END IF;
END //
DELIMITER ;

-- Procedura de adaugare a unui sesiuni noi
DELIMITER //
CREATE PROCEDURE create_session (
    IN username varchar(64),
    IN token varchar(256),
    OUT out_ex_date datetime)
BEGIN
    SET out_ex_date = ADDDATE(sysdate(), INTERVAL 1 WEEK);

    INSERT
        INTO sessions
        VALUES (
            username,
            token,
            out_ex_date
        );
    COMMIT;
END //
DELIMITER ;

-- Procedura pentru stergea sesiunilor active, atunci cand una este adaugata
DELIMITER //
CREATE PROCEDURE delete_sessions (
    IN username varchar(64))
BEGIN
    DELETE
        FROM sessions s
        WHERE s.username = username
    ;
    COMMIT;
END //
DELIMITER ;

-- Procedura pentru selectarea tuturor intrebarilor
DELIMITER //
CREATE PROCEDURE select_quizzes ()
BEGIN
    SELECT * FROM quizzes
    ;
END //
DELIMITER ;

-- Procedura pentru stergerea unei intrebari dupa id
DELIMITER //
CREATE PROCEDURE delete_quiz (
    IN id integer)
BEGIN
    DELETE
        FROM quizzes q
        WHERE q.id = id
    ;
    COMMIT;
END //
DELIMITER ;

-- Procedura pentru adaugarea unei intrebari
DELIMITER //
CREATE PROCEDURE add_quiz (
    IN in_question varchar(256),
    IN in_correct_answer varchar(256),
    IN in_wrong_answer_1 varchar(256),
    IN in_wrong_answer_2 varchar(256))
BEGIN
    INSERT
        INTO quizzes(question, correct_answer, wrong_answer_1, wrong_answer_2)
        VALUES(in_question, in_correct_answer, in_wrong_answer_1, in_wrong_answer_2)
    ;
    COMMIT;
END //
DELIMITER ;
