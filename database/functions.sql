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
