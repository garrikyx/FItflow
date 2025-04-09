-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `leaderboards`;

-- Use the leaderboards database
USE `leaderboards`;

-- Create the leaderboards table

DROP TABLE IF EXISTS `leaderboards`;
CREATE TABLE IF NOT EXISTS `leaderboards` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    calories_burned FLOAT NOT NULL,
    activity_type VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (user_id)
);


-- Insert some sample data for testing
INSERT INTO leaderboards (user_id, calories_burned, activity_type, timestamp) VALUES
('4', 120, 'yoga', '2025-04-07 17:24:26'),
('5', 400, 'cycling', '2025-04-07 08:15:00'),
('6', 600, 'swimming', '2025-04-07 18:30:00'),
('7', 120, 'yoga', '2025-04-08 07:00:00'),
('8', 350, 'running', '2025-04-08 18:45:00'),
('10', 200, 'jogging', '2025-04-08 19:00:00');