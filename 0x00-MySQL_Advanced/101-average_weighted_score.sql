-- Create a stored procedure to compute and store the average weighted score for all users
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
AS
BEGIN
    **Declare variables:**
    DECLARE @average_weighted_score DECIMAL(10,2);

    **Calculate the average weighted score for each student:**
    SELECT AVG(@average_weighted_score) INTO @average_weighted_score
    FROM (
        SELECT s.student_id, s.name, SUM(sc.score * sc.weight) AS total_weighted_score
        FROM students s
        JOIN scores sc ON s.student_id = sc.student_id
        GROUP BY s.student_id, s.name
    ) AS weighted_scores;

    **Update the students table with the average weighted scores:**
    UPDATE students
    SET average_weighted_score = @average_weighted_score;
END;

