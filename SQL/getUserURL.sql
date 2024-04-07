DELIMITER //

DROP PROCEDURE IF EXISTS getUsersURLs //
CREATE PROCEDURE getUsersURLs(
    IN p_userId INT
)
BEGIN
    SELECT LONGURL, TINYURL FROM URL WHERE USERID = p_userId;
END //

DELIMITER ;