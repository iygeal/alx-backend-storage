-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Set a new delimiter to avoid confusion between procedure statements and regular SQL statements
DELIMITER $$

-- Create the stored procedure ComputeAverageWeightedScoreForUser
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_sum FLOAT;
    DECLARE avg_weighted_score FLOAT;

    -- Calculate the total weight for the user's projects
    SELECT SUM(p.weight) INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Calculate the weighted sum of the scores
    SELECT SUM(c.score * p.weight) INTO weighted_sum
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;

    -- Compute the average weighted score
    SET avg_weighted_score = weighted_sum / total_weight;

    -- Update the average_score in the users table
    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id;
END$$

-- Reset the delimiter back to the default
DELIMITER ;
