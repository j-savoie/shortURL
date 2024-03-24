DELIMITER //

DROP PROCEDURE IF EXISTS getUsersURLs //
CREATE PROCEDURE getUsersURLs(
    IN userId INT
)
BEGIN
    IF EXISTS (SELECT 1 FROM USER WHERE ID = userId) THEN
        SELECT LONGURL, TINYURL
        FROM URL
        WHERE USERID = userId;
    ELSE
        SELECT 'User does not exist.' AS 'Error';
    END IF;
END //

DELIMITER ;