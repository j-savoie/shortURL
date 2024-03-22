DELIMITER //

DROP PROCEDURE IF EXISTS getAllURL //

CREATE PROCEDURE getAllURL(
    IN longUrl VARCHAR(256)
)
BEGIN
    IF EXISTS (SELECT 1 FROM URL WHERE URL = longUrl) THEN
        SELECT TINYURL
        FROM URL
        WHERE URL = longUrl;
    ELSE
        SELECT 'No short URLs found for the given long URL.' AS 'Error';
    END IF;
END //

DELIMITER ;