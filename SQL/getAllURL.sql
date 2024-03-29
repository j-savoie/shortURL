DELIMITER //

DROP PROCEDURE IF EXISTS getAllURL //

CREATE PROCEDURE getAllURL(
    IN longUrl VARCHAR(256)
)
BEGIN
    SELECT TINYURL FROM URL WHERE LONGURL = longUrl;
END //

DELIMITER ;