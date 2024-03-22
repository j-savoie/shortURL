DELIMITER //

DROP PROCEDURE IF EXISTS removeURL //

CREATE PROCEDURE removeURL(
    IN userID INT,
    IN shortUrl VARCHAR(265)
)
BEGIN
    IF EXISTS (SELECT 1 FROM USER WHERE ID = userID) THEN
        IF EXISTS (SELECT 1 FROM URL WHERE USERID = userID AND TINYURL = shortUrl) THEN
            DELETE FROM URL WHERE USERID = userID AND TINYURL = shortUrl;
            SELECT 'Short URL removed successfully.' AS 'Status';
        ELSE
            SELECT 'Short URL does not exist for the given user.' AS 'Error';
        END IF;
    ELSE
        SELECT 'User does not exist.' AS 'Error';
    END IF;
END //

DELIMITER ;
