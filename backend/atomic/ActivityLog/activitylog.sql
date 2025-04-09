-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Mar 31, 2025 at 05:04 AM
-- Server version: 5.7.44
-- PHP Version: 8.2.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `activitylog`
--
CREATE DATABASE IF NOT EXISTS `activitylog`;
USE `activitylog`;
-- --------------------------------------------------------

--
-- Table structure for table `activitylog`
--
DROP TABLE IF EXISTS `activitylog`;

CREATE TABLE `activitylog` (
  `id` int(11) NOT NULL,
  `userId` varchar(50) NOT NULL,
  `exerciseType` varchar(50) NOT NULL,
  `duration` int(11) NOT NULL,
  `intensity` varchar(50) NOT NULL,
  `caloriesBurned` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `activitylog`
--

INSERT INTO `activitylog` (`id`, `userId`, `exerciseType`, `duration`, `intensity`, `caloriesBurned`, `timestamp`) VALUES
(1, '4', 'yoga', 30, 'low', 120, '2025-03-26 17:24:26'),
(2, '5', 'yoga', 30, 'low', 120, '2025-03-26 17:35:15'),
(3, '6', 'Run', 30, 'low', 120, '2025-03-26 17:43:22'),
(4, '7', 'walk', 40, 'low', 320, '2025-03-26 17:43:36'),
(5, '10', 'jogging', 40, 'low', 320, '2025-03-26 17:43:56'),
(6, '4', 'jogging', 40, 'low', 320, '2025-03-26 17:45:51'),
(7, '4', 'running', 40, 'low', 320, '2025-03-26 17:45:59'),
(8, '4', 'skating', 40, 'low', 320, '2025-03-26 17:46:05'),
(9, '4', 'skating', 40, 'low', 320, '2025-03-26 17:57:05'),
(10, '4', 'running', 40, 'low', 320, '2025-03-26 17:57:12'),
(11, '4', 'jogging', 40, 'low', 320, '2025-03-26 17:57:15'),
(12, '4', 'studying', 40, 'low', 320, '2025-03-26 17:57:19'),
(13, '4', 'studying', 40, 'low', 320, '2025-03-26 18:00:39');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activitylog`
--
ALTER TABLE `activitylog`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activitylog`
--
ALTER TABLE `activitylog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
