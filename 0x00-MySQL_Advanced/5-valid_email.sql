-- Task: Create a trigger that resets valid_email only when the email has been changed

DELIMITER //

CREATE TRIGGER reset_valid_email_before_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email is changing
    IF NEW.email <> OLD.email THEN
        -- Reset valid_email to 0
        SET NEW.valid_email = 0;
    END IF;
END;

DELIMITER ;

-- End of Task SQL script
