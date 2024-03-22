DELIMITER //

DROP PROCEDURE IF EXISTS getURL //

CREATE PROCEDURE getURL(
    IN tinyUrl VARCHAR(256)
)
BEGIN
    DECLARE longUrl VARCHAR(256);

    -- Check if the provided short URL exists
    IF EXISTS (SELECT 1 FROM URL WHERE TINYURL = tinyUrl) THEN
        -- Retrieve the long URL associated with the short URL
        SELECT URL INTO longUrl FROM URL WHERE TINYURL = tinyUrl;
        SELECT longUrl AS 'Long URL';
    ELSE
        SELECT 'Short URL does not exist.' AS 'Error';
    END IF;
END //

DELIMITER ;
