DELIMITER //

DROP PROCEDURE IF EXISTS getUserID //

CREATE PROCEDURE getUserID(
    IN username VARCHAR(100)
)
BEGIN
    select ID from USER where UNAME = username;
END //

DELIMITER ;