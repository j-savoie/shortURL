DELIMITER //

CREATE PROCEDURE addURL(
    IN userId INT,
    IN url VARCHAR(256),
    IN tinyUrl VARCHAR(256)
)
BEGIN
    IF EXISTS (SELECT 1 FROM USER WHERE ID = userId) THEN
        INSERT INTO URL (URL, TINYURL, USERID) VALUES (url, tinyUrl, userId);
        
        SELECT 'URL added successfully.' AS 'Status';
    ELSE
        SELECT 'User does not exist.' AS 'Error';
    END IF;
END //

DELIMITER ;
