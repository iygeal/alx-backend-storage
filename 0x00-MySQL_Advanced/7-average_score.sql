-- Creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Set the delimiter to something other than the default `;`
DELIMITER //

-- Create the stored procedure
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Update the user's average score by calculating the average from the corrections table
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE corrections.user_id = user_id
    )
    WHERE id = user_id;
END //

-- Reset the delimiter back to `;`
DELIMITER ;

