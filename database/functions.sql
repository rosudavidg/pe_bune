-- Selectarea bazei de date
use pe_bune;

-- Functia primeste token-ul si verifica daca exista in baza de date
DELIMITER //
CREATE FUNCTION activation_token_exists (
    in_token varchar(64))
RETURNS BOOLEAN
BEGIN
    DECLARE cnt integer;
    DECLARE ans boolean;

    SELECT
        COUNT(*) INTO cnt
        FROM activations
        WHERE token = in_token
    ;

    IF cnt > 0 THEN
        SET ans = true;
    ELSE
        SET ans = false;
    END IF;

    RETURN ans;
END //
DELIMITER ;

-- Functia primeste username-ul si creeaza un joc
DELIMITER //
CREATE FUNCTION create_game_function (
    in_username varchar(64))
RETURNS int
BEGIN
    DECLARE varCategory varchar(256);
    DECLARE finished INTEGER DEFAULT 0;
    DECLARE out_game_id int;
    
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


    RETURN out_game_id;
END //
DELIMITER ;
