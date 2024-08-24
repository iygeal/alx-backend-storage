--- Creates a stored procedure ComputeAverageScoreForUser
--- that computes and store the average score for a student

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate the average score for the user
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the user's average score in the users table
    UPDATE users
    SET average_score = IFNULL(avg_score, 0)
    WHERE id = user_id;

END //

DELIMITER ;
