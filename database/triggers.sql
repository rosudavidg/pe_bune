-- Selectarea bazei de date
use pe_bune;

-- Trigger pentru activarea unui cont
DELIMITER //
CREATE TRIGGER delete_activation
    AFTER DELETE
    ON activations FOR EACH ROW
BEGIN
    UPDATE users
        SET activated = true
        WHERE email = old.email
    ;
END //
DELIMITER ;
