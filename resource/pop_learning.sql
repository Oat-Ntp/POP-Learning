-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 17, 2024 at 04:55 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pop_learning`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `tel` varchar(11) NOT NULL,
  `birth_date` date NOT NULL,
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('admin') NOT NULL DEFAULT 'admin',
  `adminimage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `first_name`, `last_name`, `username`, `email`, `tel`, `birth_date`, `registration_date`, `password`, `gender`, `role`, `adminimage`) VALUES
(1, 'Admin', 'System', 'admin', 'admin@gmail.com', '0923162131', '2024-05-09', '2024-05-27 00:00:00', 'Admin123', 'Male', 'admin', '../static/img/updated/admin/oat.jpg'),
(7, 'Admin', 'Test', 'admintest', 'admin@example.com', '0899148666', '2024-05-26', '2024-05-30 23:00:37', 'Test1234', 'Male', 'admin', '../static/img/updated/admin/instructor-2.jpg'),
(26, 'Adminnnnnnn', 'Oat', 'adoat', 'oat.500@gmail.com', '0986358476', '2024-06-05', '2024-06-05 00:00:00', 'Oat12345', 'Male', 'admin', '../static/img/avatars/avatar-1.jpg'),
(28, 'Adminnnnnnn', 'aot', 'aotntp7735', 'oat.5001@gmail.com', '0986358476', '2024-06-11', '2024-06-22 17:39:33', 'Aot12345', 'Male', 'admin', '../static/img/updated/admin/pic-8.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `icon` varchar(200) DEFAULT NULL,
  `name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `icon`, `name`) VALUES
(1, 'fa-solid fa-chart-simple', 'Power BI'),
(2, 'fa-brands fa-python', 'Python'),
(4, 'fa-brands fa-java', 'Java Script');

-- --------------------------------------------------------

--
-- Table structure for table `choices`
--

CREATE TABLE `choices` (
  `id` int(11) NOT NULL,
  `question_id` int(11) DEFAULT NULL,
  `choice_text` varchar(255) NOT NULL,
  `answer` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `choices`
--

INSERT INTO `choices` (`id`, `question_id`, `choice_text`, `answer`) VALUES
(33, 9, 'true', 1),
(34, 9, 'false', 0),
(35, 9, 'false', 0),
(36, 9, 'false', 0);

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `featured_image` text DEFAULT NULL,
  `featured_video` varchar(300) DEFAULT NULL,
  `title` varchar(500) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `instructor_id` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `description` text NOT NULL,
  `language` varchar(50) DEFAULT NULL,
  `deadline` varchar(100) DEFAULT NULL,
  `slug` varchar(500) DEFAULT NULL,
  `status` enum('PUBLISH','DRAFT') DEFAULT NULL,
  `certificate` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `featured_image`, `featured_video`, `title`, `created_at`, `instructor_id`, `category_id`, `description`, `language`, `deadline`, `slug`, `status`, `certificate`) VALUES
(4, 'static/img/updated/course\\PowerBI.png', 'hEMkB5wngSc', 'Power BI', '2024-06-22 10:48:58', 15, 1, 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', 'Thai', 'Life Time', 'PowerBi', 'PUBLISH', 'Yes'),
(7, 'static/img/updated/course\\photo-17.jpg', 'HydhEezfuFY', 'Python Test', '2024-06-22 10:49:11', 9, 2, 'qweqrasd', 'Thai', 'Life Time', 'Python', 'PUBLISH', 'Yes'),
(8, 'static/img/updated/course\\post-14.jpg', '3cTVjPdP8ps', 'CSS', '2024-06-23 16:25:33', 22, 4, 'gregetr', 'Thai', 'Life Time', 'css', 'PUBLISH', 'Yes'),
(10, '../static/img/uploads/course/cover-21.jpg', 'FMPpaTFdL2k', 'Java', '2024-06-21 09:27:18', 22, 4, 'afdsfsgsgs', 'Thai', 'Life Time', 'java-script', 'PUBLISH', 'Yes');

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `tel` varchar(11) NOT NULL,
  `birth_date` date NOT NULL,
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('instructor') NOT NULL DEFAULT 'instructor',
  `instructorimage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`id`, `first_name`, `last_name`, `username`, `email`, `tel`, `birth_date`, `registration_date`, `password`, `gender`, `role`, `instructorimage`) VALUES
(9, 'Teacher', 'Test', 'teacher', 'teacher@gmail.com', '09472845739', '2024-05-17', '2024-05-30 23:10:41', 'Test1234', 'Male', 'instructor', '../static/img/avatars/ploy.jpg'),
(15, 'Instructor', 'System', 'Instructor', 'instructor@gmail.com', '0899148666', '2024-05-08', '2024-06-05 21:12:56', 'In123456', 'Female', 'instructor', '../static/img/updated/instructor/instructor-15.jpg'),
(22, 'teaaaaaa', 'cherrrrr', 'tea123', 'teacher1@gmail.com', '0978365827', '2024-06-05', '2024-06-05 23:47:18', 'Tea12345', 'Male', 'instructor', '../static/img/updated/instructor/instructor-12.jpg'),
(24, 'Tamonpun', 'Intawong', 'ploy555', 'ploy123@gmail.com', '0923162131', '2024-06-12', '2024-06-22 17:41:20', 'Ploy1234', 'Female', 'instructor', '../static/img/uploads/instructor/pic-7.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `lesson`
--

CREATE TABLE `lesson` (
  `lesson_id` int(11) NOT NULL,
  `lesson_name` varchar(255) NOT NULL,
  `lesson_date` datetime NOT NULL DEFAULT current_timestamp(),
  `course_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lesson`
--

INSERT INTO `lesson` (`lesson_id`, `lesson_name`, `lesson_date`, `course_id`) VALUES
(1, 'Power Bi มีประโยชน์ยังไง?', '2024-06-17 22:38:56', 4),
(3, 'การใช้งาน Power Bi เบื้องต้น', '2024-06-17 22:39:00', 4),
(6, 'test', '2024-06-27 11:29:18', 7),
(9, 'บทที่1', '2024-06-27 11:29:45', 8),
(10, 'Java บทที่ 1', '2024-07-01 17:25:13', 10);

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

CREATE TABLE `question` (
  `question_id` int(11) NOT NULL,
  `quiz_id` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `question_name` varchar(255) NOT NULL,
  `choice_a` varchar(255) NOT NULL,
  `choice_b` varchar(255) NOT NULL,
  `choice_c` varchar(255) NOT NULL,
  `choice_d` varchar(255) NOT NULL,
  `correct_answer` enum('a','b','c','d') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `question`
--

INSERT INTO `question` (`question_id`, `quiz_id`, `score`, `question_name`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `correct_answer`) VALUES
(1, 9, 1, 'ประเทศใดมีประชากรมากที่สุดในโลก?', 'อินเดีย', 'สหรัฐอเมริกา', 'จีน', 'อินโดนีเซีย', 'c'),
(2, 9, 1, 'ใครเป็นประธานาธิบดีคนแรกของสหรัฐอเมริกา?', 'โธมัส เจฟเฟอร์สัน', 'จอร์จ วอชิงตัน', 'อับราฮัม ลินคอล์น', 'แอนดรูว์ แจ็คสัน', 'b'),
(3, 9, 1, 'การปฏิวัติฝรั่งเศสเกิดขึ้นในปีใด?', '1789', '1799', '1804', '1815', 'a'),
(4, 9, 1, 'อะไรคือธาตุที่เบาที่สุดในตารางธาตุ?', 'ฮีเลียม', 'ไฮโดรเจน', 'ลิเทียม', 'เบริลเลียม', 'b'),
(5, 9, 1, 'ใครเป็นผู้เขียนหนังสือ \"แฮร์รี่ พอตเตอร์\"?', 'เจ.เค. โรว์ลิง', 'จอร์จ อาร์.อาร์. มาร์ติน', 'เจ.อาร์.อาร์. โทลคีน', 'สตีเฟน คิง', 'a'),
(6, 16, 1, 'ergeryertytr', 'T', 'F', 'F', 'F', 'b'),
(7, 16, 1, 'บริษัทใดเป็นผู้พัฒนาระบบปฏิบัติการ windowsssssssss', 'Microsoft 555', 'Apple 222', 'NASA 1112', 'Google 433', 'a'),
(8, 16, 1, 'ในยุคเริ่มต้นระบบปฏิบัติการ Windows ใช้คำสั่งใดในการนำเข้าข้อมูล', 'คำสั่ง', 'คำสั่ง Terminal', 'คำสั่ง DOS', 'คำสั่ง เสียง', 'c'),
(9, 16, 1, 'ระบบปฏิบัติการ Windows ถูกสร้างขึ้นในปี ค.ศ. ใด', '1985', '2000', '2001', '2005', 'b'),
(10, 17, 1, 'wqrr', 'tert', 'ytry', 'ytyt', 'tt', 'd');

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

CREATE TABLE `quiz` (
  `quiz_id` int(11) NOT NULL,
  `quiz_name` varchar(100) DEFAULT NULL,
  `lesson_id` int(11) NOT NULL,
  `passing_percentage` int(11) DEFAULT NULL,
  `quiz_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`quiz_id`, `quiz_name`, `lesson_id`, `passing_percentage`, `quiz_date`) VALUES
(9, 'Pre-Test', 1, 60, '2024-06-13 22:34:34'),
(16, 'Post-Test', 1, 50, '2024-06-16 16:49:15'),
(17, 'Pre-Test', 3, 30, '2024-06-16 16:50:31'),
(18, 'Post-Test', 3, 40, '2024-06-16 21:41:48'),
(19, 'Pre-Test', 6, 50, '2024-06-28 01:10:09'),
(20, 'weqrq', 10, 20, '2024-06-28 01:10:21');

-- --------------------------------------------------------

--
-- Table structure for table `quiz_attempts`
--

CREATE TABLE `quiz_attempts` (
  `attempt_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `quiz_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `question_count` int(11) DEFAULT NULL,
  `attempt_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `passed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz_attempts`
--

INSERT INTO `quiz_attempts` (`attempt_id`, `user_id`, `quiz_id`, `lesson_id`, `score`, `question_count`, `attempt_date`, `passed`) VALUES
(11, 31, 9, 1, 4, 5, '2024-07-15 15:24:25', 1),
(12, 44, 9, 1, 4, 5, '2024-07-16 15:06:08', 1);

-- --------------------------------------------------------

--
-- Table structure for table `quiz_video`
--

CREATE TABLE `quiz_video` (
  `video_id` int(11) NOT NULL,
  `title` text DEFAULT '-',
  `youtube_link` text DEFAULT '-',
  `description` text DEFAULT '-',
  `time_duration` text DEFAULT '-',
  `preview` tinyint(1) DEFAULT 0,
  `video_image` text DEFAULT '-',
  `quiz_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz_video`
--

INSERT INTO `quiz_video` (`video_id`, `title`, `youtube_link`, `description`, `time_duration`, `preview`, `video_image`, `quiz_id`, `lesson_id`) VALUES
(1, '-', '-', '-', '-', 0, '-', 9, 1),
(2, '-', '-', '-', '-', 0, '-', 17, 3),
(13, '-', '-', '-', '-', 0, '-', 18, 3),
(17, 'workshop เบื้องต้น สำหรับ Power BI สำหรับผู้เริ่มศึกษา', 'VgGBxnlhYAk', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', '25', 0, '../static/img/updated/video_img/photo-35.jpg', NULL, 1),
(18, '-', '-', '-', '-', 0, '-', 16, 1),
(33, '-', '-', '-', '-', 0, '-', 19, 9),
(34, '-', '-', '-', '-', 0, '-', 19, 10),
(36, 'test', '-Uep2fZiJss', 'wqeqr', '14', 0, '../static/img/uploads/video_img/coming_soon.jpg', NULL, 6);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `birth_date` date NOT NULL,
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('user') NOT NULL DEFAULT 'user',
  `userimage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `username`, `email`, `birth_date`, `registration_date`, `password`, `gender`, `role`, `userimage`) VALUES
(20, 'user555', 'user1', 'user1', 'user@gmail.com', '2024-05-15', '2024-05-27 00:00:00', 'User1234', 'Male', 'user', '../static/img/avatars/pic-8.jpg'),
(31, 'Tamonpun', 'Intawong', 'ploy555', 'ploy@gmail.com', '2024-02-15', '2024-05-29 00:00:00', 'Ploy1234', 'Female', 'user', '../static/img/avatars/ploy.jpg'),
(33, 'user', 'user', 'usertest', 'user1@gmail.com', '2024-05-15', '2024-05-29 23:03:33', 'User1111', 'Male', 'user', '../static/img/avatars/pic-1.jpg'),
(39, 'ธนิตา', 'อาจเอี่ยม', 'nam111', 'nam@gmail.com', '2024-06-05', '2024-06-05 23:48:16', 'Nam12345', 'Male', 'user', '../static/img/avatars/avatar-4.jpg'),
(41, 'user', 'test', 'testuser123', 'user000@gmail.com', '2024-06-22', '2024-06-22 17:42:52', 'Test1234', 'Male', 'user', '../static/img/updated/user/pic-2.jpg'),
(44, 'ณัฐภัทร', 'ปานเกลี้ยง', 'aotkub7735', 'nattapat.aot7735@gmail.com', '2024-07-02', '2024-07-06 22:56:58', 'Aot12345', 'Male', 'user', '../static/img/updated/user/pic-4.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `user_enroll`
--

CREATE TABLE `user_enroll` (
  `enroll_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `enroll_date` datetime NOT NULL DEFAULT current_timestamp(),
  `is_completed` tinyint(1) NOT NULL DEFAULT 0,
  `completed_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_enroll`
--

INSERT INTO `user_enroll` (`enroll_id`, `user_id`, `course_id`, `enroll_date`) VALUES
(2, 39, 8, '2024-07-02 22:52:08'),
(3, 33, 4, '2022-06-14 21:03:05'),
(4, 39, 4, '2023-05-24 21:18:20'),
(12, 20, 4, '2024-06-25 01:19:33'),
(29, 31, 10, '2024-07-06 16:16:56'),
(31, 31, 7, '2024-07-06 16:22:55'),
(33, 31, 4, '2024-07-06 16:31:52'),
(35, 44, 4, '2024-07-08 16:36:12');

-- --------------------------------------------------------

--
-- Table structure for table `video_attempts`
--

CREATE TABLE `video_attempts` (
  `attempt_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `video_id` int(11) NOT NULL,
  `lesson_id` int(11) NOT NULL,
  `attempt_date` datetime NOT NULL,
  `passed` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `choices`
--
ALTER TABLE `choices`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_id` (`instructor_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `lesson`
--
ALTER TABLE `lesson`
  ADD PRIMARY KEY (`lesson_id`),
  ADD KEY `lesson_ibfk_1` (`course_id`);

--
-- Indexes for table `question`
--
ALTER TABLE `question`
  ADD PRIMARY KEY (`question_id`),
  ADD KEY `question_ibfk_1` (`quiz_id`);

--
-- Indexes for table `quiz`
--
ALTER TABLE `quiz`
  ADD PRIMARY KEY (`quiz_id`),
  ADD KEY `quiz_ibfk_1` (`lesson_id`);

--
-- Indexes for table `quiz_attempts`
--
ALTER TABLE `quiz_attempts`
  ADD PRIMARY KEY (`attempt_id`),
  ADD KEY `fk_lesson_id` (`lesson_id`),
  ADD KEY `fk_quiz_id` (`quiz_id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `quiz_video`
--
ALTER TABLE `quiz_video`
  ADD PRIMARY KEY (`video_id`),
  ADD KEY `quiz_video_ibfk_1` (`quiz_id`),
  ADD KEY `quiz_video_ibfk_2` (`lesson_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_enroll`
--
ALTER TABLE `user_enroll`
  ADD PRIMARY KEY (`enroll_id`),
  ADD KEY `enroll_ibfk_1` (`user_id`),
  ADD KEY `enroll_ibfk_2` (`course_id`);

--
-- Indexes for table `video_attempts`
--
ALTER TABLE `video_attempts`
  ADD PRIMARY KEY (`attempt_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `lesson_id` (`lesson_id`),
  ADD KEY `video_attempts_ibfk_2` (`video_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `choices`
--
ALTER TABLE `choices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=70;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `lesson`
--
ALTER TABLE `lesson`
  MODIFY `lesson_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `question`
--
ALTER TABLE `question`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `quiz`
--
ALTER TABLE `quiz`
  MODIFY `quiz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `quiz_attempts`
--
ALTER TABLE `quiz_attempts`
  MODIFY `attempt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `quiz_video`
--
ALTER TABLE `quiz_video`
  MODIFY `video_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `user_enroll`
--
ALTER TABLE `user_enroll`
  MODIFY `enroll_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `video_attempts`
--
ALTER TABLE `video_attempts`
  MODIFY `attempt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `courses_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `lesson`
--
ALTER TABLE `lesson`
  ADD CONSTRAINT `lesson_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `quiz`
--
ALTER TABLE `quiz`
  ADD CONSTRAINT `quiz_ibfk_1` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`lesson_id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `quiz_attempts`
--
ALTER TABLE `quiz_attempts`
  ADD CONSTRAINT `fk_lesson_id` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`lesson_id`),
  ADD CONSTRAINT `fk_quiz_id` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`),
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `quiz_video`
--
ALTER TABLE `quiz_video`
  ADD CONSTRAINT `quiz_video_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `quiz_video_ibfk_2` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`lesson_id`) ON DELETE CASCADE;

--
-- Constraints for table `user_enroll`
--
ALTER TABLE `user_enroll`
  ADD CONSTRAINT `enroll_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enroll_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `video_attempts`
--
ALTER TABLE `video_attempts`
  ADD CONSTRAINT `video_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `video_attempts_ibfk_2` FOREIGN KEY (`video_id`) REFERENCES `quiz_video` (`video_id`),
  ADD CONSTRAINT `video_attempts_ibfk_3` FOREIGN KEY (`lesson_id`) REFERENCES `lessons` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
