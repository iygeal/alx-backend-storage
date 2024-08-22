-- Task 0: Write a SQL script that creates a table `users`
-- The table should have the following attributes:
-- 1. `id` as an integer, never null, auto-increment, and primary key
-- 2. `email` as a string (255 characters), never null, and unique
-- 3. `name` as a string (255 characters)
-- The script should not fail if the table already exists
-- The script should be executable on any database

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    PRIMARY KEY (id)
);

-- End of Task 0 script
