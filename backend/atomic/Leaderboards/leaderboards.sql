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
('4', 250.5, 'running', '2023-03-25 10:30:00'),
('6', 180.2, 'cycling', '2023-03-25 11:15:00'),
('7', 320.7, 'swimming', '2023-03-25 14:45:00'),
('4', 150.3, 'walking', '2023-03-26 09:20:00'),
('10', 280.1, 'running', '2023-03-26 16:30:00'); 