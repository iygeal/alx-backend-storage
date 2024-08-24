-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables
    DECLARE done INT DEFAULT FALSE;
    DECLARE uid INT;

    -- Declare a cursor to iterate over each user
    DECLARE cur CURSOR FOR SELECT id FROM users;

    -- Declare a NOT FOUND handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Start loop
    user_loop: LOOP
        FETCH cur INTO uid;

        -- Exit loop if no more rows
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Compute the average weighted score for the current user
        CALL ComputeAverageWeightedScoreForUser(uid);
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

DELIMITER ;
