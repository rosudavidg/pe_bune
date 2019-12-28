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
        INTO users (
            username,
            password,
            email,
            first_name,
            last_name,
            level,
            experience,
            created_date,
            activated
        )
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
    IN in_token varchar(64),
    OUT out_ans boolean)
BEGIN

    SELECT activation_token_exists(in_token) INTO out_ans;

    IF out_ans = TRUE THEN
        DELETE
            FROM activations
            WHERE token = in_token
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
    IN in_username varchar(64))
BEGIN
    DELETE
        FROM sessions
        WHERE username = in_username
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
    IN in_id integer)
BEGIN
    DELETE
        FROM quizzes
        WHERE id = in_id
    ;
    COMMIT;
END //
DELIMITER ;

-- Procedura pentru adaugarea unei intrebari
DELIMITER //
CREATE PROCEDURE add_quiz (
    IN in_category varchar(256),
    IN in_question varchar(256),
    IN in_correct_answer varchar(256),
    IN in_wrong_answer_1 varchar(256),
    IN in_wrong_answer_2 varchar(256))
BEGIN
    INSERT
        INTO quizzes(category, question, correct_answer, wrong_answer_1, wrong_answer_2)
        VALUES(in_category, in_question, in_correct_answer, in_wrong_answer_1, in_wrong_answer_2)
    ;
    COMMIT;
END //
DELIMITER ;

-- Procedura pentru verificarea unei sesiuni
DELIMITER //
CREATE PROCEDURE check_token (
    IN in_token varchar(256),
    OUT out_valid boolean)
BEGIN
    DECLARE counter integer;
    DECLARE dt datetime;

    SELECT
        COUNT(*), expiration_date
    INTO
        counter, dt
    FROM
        sessions
    WHERE
        token = in_token
    ;

    IF counter = 1 THEN
        IF sysdate() < dt THEN
            SET out_valid = true;
        ELSE
            SET out_valid = false;
            END IF;
    ELSE
        SET out_valid = false;
    END IF;

END //
DELIMITER ;

-- Procedura primeste username-ul si intoarce daca contul este admin sau nu
DELIMITER //
CREATE PROCEDURE is_user_admin (
    IN in_username varchar(64),
    OUT out_is_admin boolean)
BEGIN
    DECLARE counter integer;

    SELECT
        COUNT(*) INTO counter
        FROM users
        WHERE username = in_username
        AND is_admin = TRUE
    ;

    IF counter = 1 THEN
        SET out_is_admin = TRUE;
    ELSE
        SET out_is_admin = FALSE;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE get_user (
    IN in_username varchar(64),
    OUT out_email varchar(256),
    OUT out_firstname varchar(256),
    OUT out_lastname varchar(256),
    OUT out_level int,
    OUT out_experience int)
BEGIN

    SELECT
            email, first_name, last_name, level, experience
        INTO
            out_email, out_firstname, out_lastname, out_level, out_experience
        FROM users
        WHERE username = in_username
    ;
END //
DELIMITER ;

-- Procedura primeste un username si creeaza un joc; se intoarce id-ul jocului
DELIMITER //
CREATE PROCEDURE create_game (
    IN in_username varchar(64),
    OUT out_game_id int)
BEGIN
    DECLARE varCategory varchar(256);
    DECLARE finished INTEGER DEFAULT 0;
    
    DECLARE curCategory
        CURSOR FOR
            SELECT
                DISTINCT category
                FROM quizzes
                ORDER BY rand()
                LIMIT 9
    ;

    DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

    INSERT
        INTO games (username)
        VALUES (in_username)
    ;

    SELECT LAST_INSERT_ID() INTO out_game_id;

    OPEN curCategory;

    addRandomQuiz: LOOP
        FETCH curCategory INTO varCategory;
            IF finished = 1 THEN 
                LEAVE addRandomQuiz;
            END IF;
            INSERT INTO
                games_quizzes (game_id, username, quiz_id)
            VALUES (out_game_id, in_username, (select id from quizzes where category=varCategory order by rand() LIMIT 1))
            ;
    END LOOP addRandomQuiz;

    COMMIT;
END //
DELIMITER ;

-- Procedura primeste id-ul unui joc si intoarce intrebarile
DELIMITER //
CREATE PROCEDURE get_game_quizzes (
    IN in_game_id int)
BEGIN
    SELECT quiz_id, answered, correct
        FROM games_quizzes
        WHERE game_id = in_game_id
    ;
END //
DELIMITER ;

-- Procedura primeste username-ul si intoarce daca exista deja un joc sau nu
DELIMITER //
CREATE PROCEDURE game_exists (
    IN in_username varchar(64),
    OUT out_game_exists boolean)
BEGIN
    DECLARE counter integer;

    SELECT
        COUNT(*) INTO counter
        FROM games
        WHERE username = in_username
        AND finished = FALSE
    ;

    IF counter = 0 THEN
        SET out_game_exists = FALSE;
    ELSE
        SET out_game_exists = TRUE;
    END IF;
END //
DELIMITER ;

-- Procedura primeste username-ul si intoarce id-ul jocului curent
DELIMITER //
CREATE PROCEDURE get_game_id (
    IN in_username varchar(64),
    OUT out_game_id int)
BEGIN
    DECLARE counter integer;

    SELECT
        id INTO out_game_id
        FROM games
        WHERE username = in_username
        AND finished = FALSE
    ;
END //
DELIMITER ;

-- Procedura primeste id-ul unei intrebari si intoarce categoria
DELIMITER //
CREATE PROCEDURE get_category (
    IN in_id int,
    OUT out_category varchar(256))
BEGIN
    SELECT
        category INTO out_category
        FROM quizzes
        WHERE id = in_id
    ;
END //
DELIMITER ;

-- Procedura primeste id-ul unei intrebari si intoarce raspunsurile
DELIMITER //
CREATE PROCEDURE get_quiz (
    IN in_id int,
    OUT out_question varchar(256),
    OUT out_correct varchar(256),
    OUT out_wrong_1 varchar(256),
    OUT out_wrong_2 varchar(256))
BEGIN
    SELECT
        question, correct_answer, wrong_answer_1, wrong_answer_2
        INTO out_question, out_correct, out_wrong_1, out_wrong_2
        FROM quizzes
        WHERE id = in_id
    ;
END //
DELIMITER ;
