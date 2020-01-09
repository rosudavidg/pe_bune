-- Selectarea bazei de date
use pe_bune;

-- Trigger pentru activarea unui cont
DELIMITER //
CREATE TRIGGER delete_activation
    AFTER DELETE
    ON activations FOR EACH ROW
BEGIN
    DECLARE varUsername varchar(64);
    
    UPDATE users
        SET activated = true
        WHERE email = old.email
    ;

    SELECT
        username INTO varUsername
        FROM users
        WHERE email = old.email
    ;

    INSERT
        INTO logs (username, log_time, description)
        VALUES (varUsername, sysdate(), "ACTIVATED")
    ;
END //
DELIMITER ;

-- Trigger pentru login
DELIMITER //
CREATE TRIGGER login_trigger
    AFTER INSERT
    ON sessions FOR EACH ROW
BEGIN
    INSERT
        INTO logs (username, log_time, description)
        VALUES (new.username, sysdate(), "LOGGED_IN")
    ;
END //
DELIMITER ;

-- Trigger pentru logout
DELIMITER //
CREATE TRIGGER logout_trigger
    AFTER DELETE
    ON sessions FOR EACH ROW
BEGIN
    INSERT
        INTO logs (username, log_time, description)
        VALUES (old.username, sysdate(), "LOGGED_OUT")
    ;
END //
DELIMITER ;

-- Trigger pentru inregistrare
DELIMITER //
CREATE TRIGGER register_trigger
    AFTER INSERT
    ON users FOR EACH ROW
BEGIN
    INSERT
        INTO logs (username, log_time, description)
        VALUES (new.username, sysdate(), "REGISTERED")
    ;
END //
DELIMITER ;

-- Trigger pentru joc nou
DELIMITER //
CREATE TRIGGER new_game_trigger
    AFTER INSERT
    ON games FOR EACH ROW
BEGIN
    INSERT
        INTO logs (username, log_time, description)
        VALUES (new.username, sysdate(), "STARTED_GAME")
    ;
END //
DELIMITER ;

-- Trigger pentru incheiere joc
DELIMITER //
CREATE TRIGGER finished_game_trigger
    AFTER UPDATE
    ON games FOR EACH ROW
BEGIN
    IF new.finished = TRUE THEN
        INSERT
            INTO logs (username, log_time, description)
            VALUES (new.username, sysdate(), "FINISHED_GAME")
        ;
    END IF;
END //
DELIMITER ;
