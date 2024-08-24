-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Set average_score to 0 for all users initially
    UPDATE users SET average_score = 0;

    -- Compute and update the average weighted score for all users
    UPDATE users u
    JOIN (
        SELECT c.user_id,
               SUM(c.score * p.weight) / SUM(p.weight) AS weighted_average
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        GROUP BY c.user_id
    ) AS avg_scores
    ON u.id = avg_scores.user_id
    SET u.average_score = avg_scores.weighted_average;
END //

DELIMITER ;

