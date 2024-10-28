-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 11, 2024 at 06:36 PM
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
CREATE DATABASE IF NOT EXISTS `pop_learning` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `pop_learning`;

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
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('admin') NOT NULL DEFAULT 'admin',
  `adminimage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `first_name`, `last_name`, `username`, `email`, `tel`, `registration_date`, `password`, `gender`, `role`, `adminimage`) VALUES
(1, 'Natthaphat', 'Pankaing', 'oat123', 'oat@gmail.com', '0845892234', '2024-05-27 00:00:00', 'Oat12345', 'Male', 'admin', '../static/img/updated/admin/oat.jpg');

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
(1, 'fas fa-chart-bar', 'Power BI');

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
  `slug` varchar(500) DEFAULT NULL,
  `status` enum('PUBLISH','DRAFT') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `featured_image`, `featured_video`, `title`, `created_at`, `instructor_id`, `category_id`, `description`, `slug`, `status`) VALUES
(4, 'static/img/updated/course\\PowerBI.png', 'nKAHJTJYv3s', 'Power BI Basic Training', '2024-08-17 09:33:59', 9, 1, 'วิชานี้มุ่งเน้นการเรียนรู้และพัฒนาทักษะการใช้เครื่องมือ Microsoft Power BI ในการวิเคราะห์และแสดงผลข้อมูล เพื่อสนับสนุนการตัดสินใจในองค์กร เนื้อหาจะครอบคลุมการนำเข้าข้อมูลจากแหล่งต่างๆ การทำความสะอาดและการเตรียมข้อมูล การสร้างโมเดลข้อมูล การสร้างภาพแสดงผลข้อมูลแบบ Interactive การสร้าง Dashboard รวมถึงการแชร์และเผยแพร่รายงาน นอกจากนี้ ผู้เรียนจะได้เรียนรู้แนวทางปฏิบัติที่ดีที่สุดในการจัดการและแสดงผลข้อมูลอย่างมีประสิทธิภาพ', 'PowerBi', 'PUBLISH');

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
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('instructor') NOT NULL DEFAULT 'instructor',
  `instructorimage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`id`, `first_name`, `last_name`, `username`, `email`, `tel`, `registration_date`, `password`, `gender`, `role`, `instructorimage`) VALUES
(9, 'Tamonpun', 'Intawong', 'ploy555', 'ploy@gmail.com', '09472845739', '2024-05-30 23:10:41', 'Ploy1234', 'Female', 'instructor', '../static/img/updated/instructor/ploy.jpg'),
(15, 'Nuchanart', 'Tientong', 'puy555', 'puy@gmail.com', '0899148666', '2024-06-05 21:12:56', 'Puy12345', 'Female', 'instructor', '../static/img/updated/instructor/puy.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `lesson`
--

CREATE TABLE `lesson` (
  `lesson_id` int(11) NOT NULL,
  `lesson_name` varchar(255) NOT NULL,
  `lesson_date` datetime NOT NULL DEFAULT current_timestamp(),
  `course_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lesson`
--

INSERT INTO `lesson` (`lesson_id`, `lesson_name`, `lesson_date`, `course_id`, `instructor_id`) VALUES
(1, 'บทที่ 1 Turn Data To Insigth With Power BI', '2024-07-24 20:57:00', 4, 9),
(3, 'บทที่ 2 การแปลงข้อมูลด้วย Power BI', '2024-07-25 20:58:16', 4, 9),
(12, 'บทที่ 3 ความสัมพันธ์', '2024-07-25 20:58:27', 4, 9),
(13, 'บทที่ 4 Data Visualization ใน Power BI', '2024-08-14 00:22:40', 4, 9);

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
  `correct_answer` enum('a','b','c','d') NOT NULL,
  `question_image` varchar(255) DEFAULT NULL,
  `choice_a_image` varchar(255) DEFAULT NULL,
  `choice_b_image` varchar(255) DEFAULT NULL,
  `choice_c_image` varchar(255) DEFAULT NULL,
  `choice_d_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `question`
--

INSERT INTO `question` (`question_id`, `quiz_id`, `score`, `question_name`, `choice_a`, `choice_b`, `choice_c`, `choice_d`, `correct_answer`, `question_image`, `choice_a_image`, `choice_b_image`, `choice_c_image`, `choice_d_image`) VALUES
(1, 9, 1, 'โปรแกรมใดไม่ใช่ส่วนประกอบของ Microsoft Power Platform', 'Power BI', 'Power Apps', 'Microsoft word', 'Virtual Agents', 'c', NULL, NULL, NULL, NULL, NULL),
(2, 9, 1, 'Power BI คืออะไร', 'เทคโนโลยีเพื่อใช้ในการนำข้อมูลจากแหล่งต่างๆ หลายๆแหล่งมาปรับแต่ง จัดระเบียบ สร้างความสัมพันธ์ คำนวณ เพื่อสร้างรายงาน Interactive Dashboard', 'ซอฟต์แวร์เครื่องมือในการพัฒนา Application ทางธุรกิจสำหรับ Mobile, Tablet และพัฒนา เว็บไซต์ แบบ Low Code / No Code ช่วยให้ Citizen Developer หรือผู้ที่ไม่ใช่ Programmer สามารถสร้าง App ของตนเองได้', 'เครื่องมือการทำงานร่วมกัน ผ่านการทำ Chat ให้สามารถทำงานร่วมกันและแบ่งปันข้อมูลผ่านพื้นที่ส่วนกลาง และเป็นตัวเชื่อมต่อกับ App อื่น ๆ ของ Microsoft', 'เป็นโปรแกรมประมวลผลคำเพื่องานการสร้างเอกสารได้อย่างมีประสิทธิภาพสะดวกและประหยัดเวลา เหมาะกับการพิมพ์เอกสารทุกประเภท', 'a', NULL, NULL, NULL, NULL, NULL),
(3, 9, 1, 'Power BI สามารถนำเข้าข้อมูลจากไฟล์ฐานข้อมูลแบบใดได้บ้าง', 'On-premise', 'Cloud', 'ถูกทั้งข้อ 1 และ 2', 'ผิดทุกข้อ', 'c', NULL, NULL, NULL, NULL, NULL),
(4, 9, 1, 'Software ในกลุ่ม Power BI ประกอบไปด้วยกี่ส่วน', '2 ส่วน', '3 ส่วน', '4 ส่วน', '5 ส่วน', 'b', NULL, NULL, NULL, NULL, NULL),
(5, 9, 1, 'Power BI ประกอบด้วยส่วนประกอบหลักใดบ้าง', 'Power BI Desktop', 'Power BI Mobile', 'Power BI Service', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(6, 9, 1, 'Microsoft ให้พื้นที่สำหรับใช้งานฟรีเท่าไร', '10 GB', '15 GB', '25 GB', '30 GB', 'b', NULL, NULL, NULL, NULL, NULL),
(7, 9, 1, 'Data ประเภทใดไม่สามารถนำมาใช้ได้ในโปรแกรม Power BI', 'Text', 'Excel', 'CSV', 'ไม่มีคำตอบที่ถูกต้อง', 'd', NULL, NULL, NULL, NULL, NULL),
(8, 9, 1, 'Power BI ใช้แหล่งข้อมูลอะไรในการสร้างโมเดลข้อมูล?', 'แหล่งข้อมูลภายนอก', 'ข้อมูลที่นำเข้าจากไฟล์ CSV', 'ข้อมูลที่เชื่อมต่อแบบออนไลน์', 'ทั้งหมดข้างต้น', 'd', NULL, NULL, NULL, NULL, NULL),
(9, 9, 1, 'การทำให้ข้อมูลพร้อมใช้งายโดยการ แปร เปลี่ยน ปรับ ลบ เรียกว่าอะไร', 'ETL', 'SQL', 'ADSL', 'CGI', 'a', NULL, NULL, NULL, NULL, NULL),
(10, 9, 1, 'ความหมายของ E ในคำว่า ETL', 'Exit', 'Evolution', 'Enhanced', 'Extract', 'd', NULL, NULL, NULL, NULL, NULL),
(11, 9, 1, 'ความหมายของ T ในคำว่า ETL', 'Transfer', 'Transform', 'Translation', 'Transaction', 'b', NULL, NULL, NULL, NULL, NULL),
(12, 9, 1, 'ความหมายของ L ในคำว่า ETL', 'Load', 'Locator', 'Lower', 'Local', 'a', NULL, NULL, NULL, NULL, NULL),
(13, 9, 1, 'ข้อใดคือ Version ของ Power BI ที่ใช้สร้างรายงาน', 'Power BI Desktop', 'Power BI Report server', 'Power BI Mobile', 'Power BI Gateway', 'a', NULL, NULL, NULL, NULL, NULL),
(14, 9, 1, 'Power BI เป็น Software ของบริษัทอะไร', 'IBMA', 'Amazon', 'Microsoft', 'Oracle', 'c', NULL, NULL, NULL, NULL, NULL),
(15, 9, 1, 'ข้อใดไม่ใช่ประเภทของการแสดงผลที่สามารถสร้างได้ใน Power BI', 'บาร์ชาร์ต', 'พายชาร์ต', 'แมพ', 'โปรแกรมประมวลผลคำ', 'd', NULL, NULL, NULL, NULL, NULL),
(16, 9, 1, 'คุณสามารถใช้ Power BI Mobile สำหรับอะไร', 'การสร้างรายงานใหม่', 'การเข้าถึงรายงานและแดชบอร์ดบนมือถือ', 'การแปลงข้อมูล', 'การเชื่อมต่อแหล่งข้อมูลใหม่', 'b', NULL, NULL, NULL, NULL, NULL),
(17, 9, 1, 'ข้อใดคือวิธีการแปลงข้อมูล ETL', 'การลบข้อมูลซ้ำ', 'การรวมข้อมูล', 'การแปลงประเภทข้อมูล', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(18, 9, 1, 'ข้อใดไม่ใช่ฟีเจอร์ของ Power BI Service', 'การสร้างรายงาน', 'การสร้างแบบฟอร์มกรอกข้อมูล', 'การแชร์แดชบอร์ด', 'การรีเฟรชข้อมูลอัตโนมัติ', 'b', NULL, NULL, NULL, NULL, NULL),
(19, 9, 1, 'Power BI คืออะไร', 'โปรแกรมแก้ไขข้อความ', 'เครื่องมือสร้างและจัดการฐานข้อมูล', 'เครื่องมือการวิเคราะห์ข้อมูลและการสร้างรายงาน', 'โปรแกรมตัดต่อภาพ', 'c', NULL, NULL, NULL, NULL, NULL),
(20, 9, 1, 'Power BI Desktop สามารถเชื่อมต่อกับแหล่งข้อมูลใดได้บ้าง', 'ฐานข้อมูล SQL', 'ไฟล์ Excel', 'เว็บไซต์', 'ทุกข้อที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(21, 16, 1, 'โปรแกรมใดไม่ใช่ส่วนประกอบของ Microsoft Power Platform', 'Power BI', 'Power Apps', 'Microsoft word', 'Virtual Agents', 'c', NULL, NULL, NULL, NULL, NULL),
(22, 16, 1, 'Power BI คืออะไร', 'เทคโนโลยีเพื่อใช้ในการนำข้อมูลจากแหล่งต่างๆ หลายๆแหล่งมาปรับแต่ง จัดระเบียบ สร้างความสัมพันธ์ คำนวณ เพื่อสร้างรายงาน Interactive Dashboard', 'ซอฟต์แวร์เครื่องมือในการพัฒนา Application ทางธุรกิจสำหรับ Mobile, Tablet และพัฒนา เว็บไซต์ แบบ Low Code / No Code ช่วยให้ Citizen Developer หรือผู้ที่ไม่ใช่ Programmer สามารถสร้าง App ของตนเองได้', 'เครื่องมือการทำงานร่วมกัน ผ่านการทำ Chat ให้สามารถทำงานร่วมกันและแบ่งปันข้อมูลผ่านพื้นที่ส่วนกลาง และเป็นตัวเชื่อมต่อกับ App อื่น ๆ ของ Microsoft', 'เป็นโปรแกรมประมวลผลคำเพื่องานการสร้างเอกสารได้อย่างมีประสิทธิภาพสะดวกและประหยัดเวลา เหมาะกับการพิมพ์เอกสารทุกประเภท', 'a', NULL, NULL, NULL, NULL, NULL),
(23, 16, 1, 'Power BI สามารถนำเข้าข้อมูลจากไฟล์ฐานข้อมูลแบบใดได้บ้าง', 'On-premise', 'Cloud', 'ถูกทั้งข้อ 1 และ 2', 'ผิดทุกข้อ', 'c', NULL, NULL, NULL, NULL, NULL),
(24, 16, 1, 'Software ในกลุ่ม Power BI ประกอบไปด้วยกี่ส่วน', '2 ส่วน', '3 ส่วน', '4 ส่วน', '5 ส่วน', 'b', NULL, NULL, NULL, NULL, NULL),
(25, 16, 1, 'Power BI ประกอบด้วยส่วนประกอบหลักใดบ้าง', 'Power BI Desktop', 'Power BI Mobile', 'Power BI Service', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(26, 16, 1, 'Microsoft ให้พื้นที่สำหรับใช้งานฟรีเท่าไร', '10 GB', '15 GB', '25 GB', '30 GB', 'b', NULL, NULL, NULL, NULL, NULL),
(27, 16, 1, 'Data ประเภทใดไม่สามารถนำมาใช้ได้ในโปรแกรม Power BI', 'Text', 'Excel', 'CSV', 'ไม่มีคำตอบที่ถูกต้อง', 'd', NULL, NULL, NULL, NULL, NULL),
(28, 16, 1, 'Power BI ใช้แหล่งข้อมูลอะไรในการสร้างโมเดลข้อมูล?', 'แหล่งข้อมูลภายนอก', 'ข้อมูลที่นำเข้าจากไฟล์ CSV', 'ข้อมูลที่เชื่อมต่อแบบออนไลน์', 'ทั้งหมดข้างต้น', 'd', NULL, NULL, NULL, NULL, NULL),
(29, 16, 1, 'การทำให้ข้อมูลพร้อมใช้งายโดยการ แปร เปลี่ยน ปรับ ลบ เรียกว่าอะไร', 'ETL', 'SQL', 'ADSL', 'CGI', 'a', NULL, NULL, NULL, NULL, NULL),
(30, 16, 1, 'ความหมายของ E ในคำว่า ETL', 'Exit', 'Evolution', 'Enhanced', 'Extract', 'd', NULL, NULL, NULL, NULL, NULL),
(31, 16, 1, 'ความหมายของ T ในคำว่า ETL', 'Transfer', 'Transform', 'Translation', 'Transaction', 'b', NULL, NULL, NULL, NULL, NULL),
(32, 16, 1, 'ความหมายของ L ในคำว่า ETL', 'Load', 'Locator', 'Lower', 'Local', 'a', NULL, NULL, NULL, NULL, NULL),
(33, 16, 1, 'ข้อใดคือ Version ของ Power BI ที่ใช้สร้างรายงาน', 'Power BI Desktop', 'Power BI Report server', 'Power BI Mobile', 'Power BI Gateway', 'a', NULL, NULL, NULL, NULL, NULL),
(34, 16, 1, 'Power BI เป็น Software ของบริษัทอะไร', 'IBMA', 'Amazon', 'Microsoft', 'Oracle', 'c', NULL, NULL, NULL, NULL, NULL),
(35, 16, 1, 'ข้อใดไม่ใช่ประเภทของการแสดงผลที่สามารถสร้างได้ใน Power BI', 'บาร์ชาร์ต', 'พายชาร์ต', 'แมพ', 'โปรแกรมประมวลผลคำ', 'd', NULL, NULL, NULL, NULL, NULL),
(36, 16, 1, 'คุณสามารถใช้ Power BI Mobile สำหรับอะไร', 'การสร้างรายงานใหม่', 'การเข้าถึงรายงานและแดชบอร์ดบนมือถือ', 'การแปลงข้อมูล', 'การเชื่อมต่อแหล่งข้อมูลใหม่', 'b', NULL, NULL, NULL, NULL, NULL),
(37, 16, 1, 'ข้อใดคือวิธีการแปลงข้อมูล ETL', 'การลบข้อมูลซ้ำ', 'การรวมข้อมูล', 'การแปลงประเภทข้อมูล', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(38, 16, 1, 'ข้อใดไม่ใช่ฟีเจอร์ของ Power BI Service', 'การสร้างรายงาน', 'การสร้างแบบฟอร์มกรอกข้อมูล', 'การแชร์แดชบอร์ด', 'การรีเฟรชข้อมูลอัตโนมัติ', 'b', NULL, NULL, NULL, NULL, NULL),
(39, 16, 1, 'Power BI คืออะไร', 'โปรแกรมแก้ไขข้อความ', 'เครื่องมือสร้างและจัดการฐานข้อมูล', 'เครื่องมือการวิเคราะห์ข้อมูลและการสร้างรายงาน', 'โปรแกรมตัดต่อภาพ', 'c', NULL, NULL, NULL, NULL, NULL),
(40, 16, 1, 'Power BI Desktop สามารถเชื่อมต่อกับแหล่งข้อมูลใดได้บ้าง', 'ฐานข้อมูล SQL', 'ไฟล์ Excel', 'เว็บไซต์', 'ทุกข้อที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(41, 17, 1, 'ข้อใดเป็น Menu แรกที่จะต้องใช้เมื่อทำงานกับ Power BI', 'Get Data', 'Transform Data', 'Modeling', 'Publish', 'a', NULL, NULL, NULL, NULL, NULL),
(42, 17, 1, 'ข้อใดเป็นนามสกุลของไฟล์ Power BI', '.pwbi', '.pbix', '.mpbi', '.pbi', 'd', NULL, NULL, NULL, NULL, NULL),
(43, 17, 1, 'การอัพเดทข้อมูลใน Power BI Desktop สามารถทำได้อย่างไร', 'อัพเดทแบบอัตโนมัติ', 'รีเฟรชข้อมูล', 'ดาวน์โหลดไฟล์ใหม่', 'สร้างไฟล์ใหม่', 'b', NULL, NULL, NULL, NULL, NULL),
(44, 17, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'a', 'que.jpg', NULL, NULL, NULL, NULL),
(45, 17, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'b', 'que2.jpg', NULL, NULL, NULL, NULL),
(46, 17, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'c', 'que3.jpg', NULL, NULL, NULL, NULL),
(47, 17, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'd', 'que4.jpg', NULL, NULL, NULL, NULL),
(48, 17, 1, 'หากข้อมูลที่ต้องการจะนำเข้าเป็นข้อมูลที่พร้อมใช้แล้วควรเลือกข้อใด', '', '', '', '', 'a', NULL, 'que5.jpg', 'que6.jpg', 'que7.jpg', 'que8.jpg'),
(49, 17, 1, 'หากข้อมูลที่ต้องการจะนำเข้าเป็นข้อมูลที่ไม่พร้อมใช้ควรเลือกข้อใด', '', '', '', '', 'b', NULL, 'que5.jpg', 'que6.jpg', 'que7.jpg', 'que8.jpg'),
(50, 17, 1, 'หากต้องการที่จะบันทึกข้อมูลที่ผ่านการ ETL แล้วควรเลือกข้อใด ', '', '', '', '', 'd', NULL, 'que9.jpg', 'que10.jpg', 'que11.jpg', 'que12.jpg'),
(51, 17, 1, 'Power Query ใน Power BI ใช้สำหรับทำอะไร?', 'การสร้างกราฟและรายงาน', 'การล้างและแปลงข้อมูล', 'การแชร์รายงาน', 'การอัปโหลดข้อมูลไปยัง Power BI Service', 'b', NULL, NULL, NULL, NULL, NULL),
(52, 17, 1, 'ฟังก์ชันใดที่ใช้ในการลบแถวคอลัมน์ใน Power Query?', 'Remove Columns', 'Remove Rows', 'Replace Values', 'Filter Rows', 'a', NULL, NULL, NULL, NULL, NULL),
(53, 17, 1, 'ข้อใดเป็นเครื่องมือที่ใช้ในการแปลงข้อมูลใน Power BI Desktop?', 'Power query', 'Power pivot', 'Power view', 'Power Map', 'a', NULL, NULL, NULL, NULL, NULL),
(54, 17, 1, 'การใช้ Power Query เพื่อแปลงข้อมูล คุณจะต้องเข้าถึงได้จากเมนูใดใน Power BI Desktop', 'home', 'Transform Data', 'Visualizations', 'Data Model', 'b', NULL, NULL, NULL, NULL, NULL),
(55, 17, 1, 'DAX ย่อมาจากอะไร?', 'Data Analysis Expressions', 'Data Analytics Explorer', 'Data Access Extension', 'Data Aggregation Expert', 'a', NULL, NULL, NULL, NULL, NULL),
(56, 17, 1, 'ข้อใดเป็นขั้นตอนพื้นฐานในการแปลงข้อมูล Power Query', 'โหลดข้อมูล', 'กรองข้อมูล', 'การเปลี่ยนประเภทข้อมูล', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(57, 17, 1, 'การเปลี่ยนชื่อคอลัมน์ใน Power Query สามารถทำได้อย่างไร?', 'คลิกขวาที่ชื่อคอลัมน์และเลือก Rename', 'ใช้คำสั่ง Replace Values', 'ใช้คำสั่ง Group By', 'แปลงคอลัมน์เป็นแถว', 'a', NULL, NULL, NULL, NULL, NULL),
(58, 17, 1, 'คุณสามารถสร้างอะไรได้บ้างใน Power BI Desktop?', 'Dashboard', 'Reports', 'Data Models', 'ทั้ง b) และ c)', 'd', NULL, NULL, NULL, NULL, NULL),
(59, 17, 1, 'การเปลี่ยนแปลงที่ทำใน Power Query จะถูกบันทึกอย่างไร', 'โดยการคลิกปุ่ม Save As', 'โดยการคลิกปุ่ม Close & Apply', 'โดยการสร้างรายงานใหม่', 'โดยการส่งไฟล์ออกเป็น CSV', 'b', NULL, NULL, NULL, NULL, NULL),
(60, 17, 1, 'การแปลงข้อมูลใน Power Query สามารถบันทึกเป็นอะไร', 'ไฟล์ PBIX', 'ไฟล์ CSV', 'ไฟล์ Excel', 'ไฟล์ PDF', 'c', NULL, NULL, NULL, NULL, NULL),
(61, 18, 1, 'ข้อใดเป็น Menu แรกที่จะต้องใช้เมื่อทำงานกับ Power BI', 'Get Data', 'Transform Data', 'Modeling', 'Publish', 'a', NULL, NULL, NULL, NULL, NULL),
(62, 18, 1, 'ข้อใดเป็นนามสกุลของไฟล์ Power BI', '.pwbi', '.pbix', '.mpbi', '.pbi', 'd', NULL, NULL, NULL, NULL, NULL),
(63, 18, 1, 'การอัพเดทข้อมูลใน Power BI Desktop สามารถทำได้อย่างไร?', 'อัพเดทแบบอัตโนมัติ', 'รีเฟรชข้อมูล', 'ดาวน์โหลดไฟล์ใหม่', 'สร้างไฟล์ใหม่', 'b', NULL, NULL, NULL, NULL, NULL),
(64, 18, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'a', 'que.jpg', NULL, NULL, NULL, NULL),
(65, 18, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'b', 'que2.jpg', NULL, NULL, NULL, NULL),
(66, 18, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'c', 'que3.jpg', NULL, NULL, NULL, NULL),
(67, 18, 1, 'จากภาพคือสัญลักษณ์ของหน้ามุมมองใด', 'Report view', 'Table view', 'Model view', 'DAX Query view', 'd', 'que4.jpg', NULL, NULL, NULL, NULL),
(68, 18, 1, 'หากข้อมูลที่ต้องการจะนำเข้าเป็นข้อมูลที่พร้อมใช้แล้วควรเลือกข้อใด', '', '', '', '', 'a', NULL, 'que5.jpg', 'que6.jpg', 'que7.jpg', 'que8.jpg'),
(69, 18, 1, 'หากข้อมูลที่ต้องการจะนำเข้าเป็นข้อมูลที่ไม่พร้อมใช้ควรเลือกข้อใด', '', '', '', '', 'b', NULL, 'que5.jpg', 'que6.jpg', 'que7.jpg', 'que8.jpg'),
(70, 18, 1, 'หากต้องการที่จะบันทึกข้อมูลที่ผ่านการ ETL แล้วควรเลือกข้อใด ', '', '', '', '', 'd', NULL, 'que9.jpg', 'que10.jpg', 'que11.jpg', 'que12.jpg'),
(71, 18, 1, 'Power Query ใน Power BI ใช้สำหรับทำอะไร?', 'การสร้างกราฟและรายงาน', 'การล้างและแปลงข้อมูล', 'การแชร์รายงาน', 'การอัปโหลดข้อมูลไปยัง Power BI Service', 'b', NULL, NULL, NULL, NULL, NULL),
(72, 18, 1, 'ฟังก์ชันใดที่ใช้ในการลบแถวคอลัมน์ใน Power Query?', 'Remove Columns', 'Remove Rows', 'Replace Values', 'Filter Rows', 'a', NULL, NULL, NULL, NULL, NULL),
(73, 18, 1, 'ข้อใดเป็นเครื่องมือที่ใช้ในการแปลงข้อมูลใน Power BI Desktop?', 'Power query', 'Power pivot', 'Power view', 'Power Map', 'a', NULL, NULL, NULL, NULL, NULL),
(74, 18, 1, 'การใช้ Power Query เพื่อแปลงข้อมูล คุณจะต้องเข้าถึงได้จากเมนูใดใน Power BI Desktop', 'home', 'Transform Data', 'Visualizations', 'Data Model', 'b', NULL, NULL, NULL, NULL, NULL),
(75, 18, 1, 'DAX ย่อมาจากอะไร?', 'Data Analysis Expressions', 'Data Analytics Explorer', 'Data Access Extension', 'Data Aggregation Expert', 'a', NULL, NULL, NULL, NULL, NULL),
(76, 18, 1, 'ข้อใดเป็นขั้นตอนพื้นฐานในการแปลงข้อมูล Power Query', 'โหลดข้อมูล', 'กรองข้อมูล', 'การเปลี่ยนประเภทข้อมูล', 'ทั้งหมดที่กล่าวมา', 'd', NULL, NULL, NULL, NULL, NULL),
(77, 18, 1, 'การเปลี่ยนชื่อคอลัมน์ใน Power Query สามารถทำได้อย่างไร?', 'คลิกขวาที่ชื่อคอลัมน์และเลือก Rename', 'ใช้คำสั่ง Replace Values', 'ใช้คำสั่ง Group By', 'แปลงคอลัมน์เป็นแถว', 'a', NULL, NULL, NULL, NULL, NULL),
(78, 18, 1, 'คุณสามารถสร้างอะไรได้บ้างใน Power BI Desktop?', 'Dashboard', 'Reports', 'Data Models', 'ทั้ง b) และ c)', 'd', NULL, NULL, NULL, NULL, NULL),
(79, 18, 1, 'การเปลี่ยนแปลงที่ทำใน Power Query จะถูกบันทึกอย่างไร', 'โดยการคลิกปุ่ม Save As', 'โดยการคลิกปุ่ม Close & Apply', 'โดยการสร้างรายงานใหม่', 'โดยการส่งไฟล์ออกเป็น CSV', 'b', NULL, NULL, NULL, NULL, NULL),
(80, 18, 1, 'การแปลงข้อมูลใน Power Query สามารถบันทึกเป็นอะไร', 'ไฟล์ PBIX', 'ไฟล์ CSV', 'ไฟล์ Excel', 'ไฟล์ PDF', 'c', NULL, NULL, NULL, NULL, NULL),
(81, 23, 1, 'Relationship ใน Power BI ใช้เพื่ออะไร?', 'การรวมข้อมูลจากตารางหลายตาราง', 'การสร้างกราฟ', 'การแชร์รายงาน', 'การเชื่อมต่อกับฐานข้อมูล', 'a', NULL, NULL, NULL, NULL, NULL),
(82, 23, 1, 'Relationship หมายถึงข้อใด', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'การจัดหน้ากระดาษ', 'การหาผลลัพธ์', 'การจัดการกับความสัมพันธ์ของตัวเลข', 'a', NULL, NULL, NULL, NULL, NULL),
(83, 23, 1, 'Fact Table หมายถึงข้อใด', 'ตารางในการวัดยอดขาย กำไร ต้นทุน', 'ตารางการเข้าเรียน', 'ตารางปฏิทิน', 'ตารางในการวัดความกว้างของถนน', 'a', NULL, NULL, NULL, NULL, NULL),
(84, 23, 1, 'เหตุใดตาราง Customer กับ Employee ถึงไม่ได้เชื่อมโยงกัน', 'เพราะไม่เกี่ยวข้องกัน', 'ตั้งชื่อไม่ตรงกัน', 'ตั้งชื่อเหมือนกัน', 'เพราะมีความปลอดภัย', 'b', NULL, NULL, NULL, NULL, NULL),
(85, 23, 1, 'ทำไมถึงต้องจัดรูปแบบของข้อมูลที่ได้มาจาก Power Query', 'เพราะความปลอดภัย', 'เพื่อความสวยงาม', 'เพื่อความเป็นระเบียบของข้อมูล', 'เพราะจะไม่มี วัน/เดือน/ปี ทศนิยม และ ,', 'd', NULL, NULL, NULL, NULL, NULL),
(86, 23, 1, 'Report View หมายถึงข้อใด', 'การเรียนรู้', 'การสรุปผลที่อยากรู้', 'การผ่อนคลาย', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'b', NULL, NULL, NULL, NULL, NULL),
(87, 23, 1, 'Data View แสดงผลในรูปแบบใด', 'รูปภาพ', 'ตาราง', 'เสียง', 'Web site', 'b', NULL, NULL, NULL, NULL, NULL),
(88, 23, 1, 'คุณสมบัติใดใน Power BI ที่ช่วยให้คุณสามารถสร้าง Relationship ระหว่างตารางได้อัตโนมัติ?', 'Auto Detect', 'Manual Mapping', 'Auto Relationship', 'Relationship Builder', 'a', NULL, NULL, NULL, NULL, NULL),
(89, 23, 1, 'Data View จะแสดงผลข้อมูลที่ได้ Get Data เข้ามาในรูปแบบใด', 'รูปแบบที่แก้ไขได้', 'รูปแบบรูปภาพ', 'รูปแบบที่อ่านได้อย่างเดียว', 'รูปแบบที่อ่านและสามารถแก้ไขได้', 'c', NULL, NULL, NULL, NULL, NULL),
(90, 23, 1, 'ตาราง Customer หมายถึงข้อใด', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'รายละเอียดการสั่งซื้อ', 'c', NULL, NULL, NULL, NULL, NULL),
(91, 23, 1, 'ตาราง Employee หมายถึงข้อใด', 'สินค้า', 'ลูกค้า', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'd', NULL, NULL, NULL, NULL, NULL),
(92, 23, 1, 'ตาราง Order Details หมายถึงข้อใด', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'a', NULL, NULL, NULL, NULL, NULL),
(93, 23, 1, 'ตาราง Products หมายถึงข้อใด', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'c', NULL, NULL, NULL, NULL, NULL),
(94, 23, 1, 'ตาราง Categories หมายถึงข้อใด', 'หมวดหมู่', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'a', NULL, NULL, NULL, NULL, NULL),
(95, 23, 1, 'ตาราง Suppliers หมายถึงข้อใด', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'ผู้ขาย', 'd', NULL, NULL, NULL, NULL, NULL),
(96, 23, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 หมวดหมู่มีหลายสินค้า', '1 สินค้ามีหลายหมวดหมู่', '1 หมวดหมู่มีหลายหมวดหมู่', '1 ผู้ขายมีหลายสินค้า', 'a', 'que13.jpg', NULL, NULL, NULL, NULL),
(97, 23, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 หมวดหมู่มีหลายสินค้า', 'ลูกค้า 1 คนสามารถสั่งซื้อได้หลายครั้ง', 'ลูกค้าหลายคนสามารถซื้อได้ 1 อย่าง', '1 ผู้ขายมีหลายสินค้า', 'b', 'que14.jpg', NULL, NULL, NULL, NULL),
(98, 23, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', 'พนักงาน 1 คนมีหลายการขาย', '1 หมวดหมู่มีหลายสินค้า', '1 ผู้ขายมีหลายสินค้า', 'พนักงาน 2 คนมี 1 การขาย', 'a', 'que15.jpg', NULL, NULL, NULL, NULL),
(99, 23, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', 'พนักงาน 1 คน มีหลายการขาย', 'สินค้า 1 ชิ้น มีหลายการสั่งซื้อ', '1 หมวดหมู่มีหลายสินค้า', '1 สินค้ามีหลายหมวดหมู่', 'b', 'que16.jpg', NULL, NULL, NULL, NULL),
(100, 23, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 ผู้ขายมีพนักงาน 1 คน', '1 ผู้ขายมี 1 สินค้า', '1 สินค้ามีหลายหมวดหมู่', '1 ผู้ขายมีหลายสินค้า', 'd', 'que17.jpg', NULL, NULL, NULL, NULL),
(101, 24, 1, 'Relationship ใน Power BI ใช้เพื่ออะไร?', 'การรวมข้อมูลจากตารางหลายตาราง', 'การสร้างกราฟ', 'การแชร์รายงาน', 'การเชื่อมต่อกับฐานข้อมูล', 'a', NULL, NULL, NULL, NULL, NULL),
(102, 24, 1, 'Relationship หมายถึงข้อใด', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'การจัดหน้ากระดาษ', 'การหาผลลัพธ์', 'การจัดการกับความสัมพันธ์ของตัวเลข', 'a', NULL, NULL, NULL, NULL, NULL),
(103, 24, 1, 'Fact Table หมายถึงข้อใด', 'ตารางในการวัดยอดขาย กำไร ต้นทุน', 'ตารางการเข้าเรียน', 'ตารางปฏิทิน', 'ตารางในการวัดความกว้างของถนน', 'a', NULL, NULL, NULL, NULL, NULL),
(104, 24, 1, 'เหตุใดตาราง Customer กับ Employee ถึงไม่ได้เชื่อมโยงกัน', 'เพราะไม่เกี่ยวข้องกัน', 'ตั้งชื่อไม่ตรงกัน', 'ตั้งชื่อเหมือนกัน', 'เพราะมีความปลอดภัย', 'b', NULL, NULL, NULL, NULL, NULL),
(105, 24, 1, 'ทำไมถึงต้องจัดรูปแบบของข้อมูลที่ได้มาจาก Power Query', 'เพราะความปลอดภัย', 'เพื่อความสวยงาม', 'เพื่อความเป็นระเบียบของข้อมูล', 'เพราะจะไม่มี วัน/เดือน/ปี ทศนิยม และ ,', 'd', NULL, NULL, NULL, NULL, NULL),
(106, 24, 1, 'Report View หมายถึงข้อใด', 'การเรียนรู้', 'การสรุปผลที่อยากรู้', 'การผ่อนคลาย', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'b', NULL, NULL, NULL, NULL, NULL),
(107, 24, 1, 'Data View แสดงผลในรูปแบบใด', 'รูปภาพ', 'ตาราง', 'เสียง', 'Web site', 'b', NULL, NULL, NULL, NULL, NULL),
(108, 24, 1, 'คุณสมบัติใดใน Power BI ที่ช่วยให้คุณสามารถสร้าง Relationship ระหว่างตารางได้อัตโนมัติ?', 'Auto Detect', 'Manual Mapping', 'Auto Relationship', 'Relationship Builder', 'a', NULL, NULL, NULL, NULL, NULL),
(109, 24, 1, 'Data View จะแสดงผลข้อมูลที่ได้ Get Data เข้ามาในรูปแบบใด', 'รูปแบบที่แก้ไขได้', 'รูปแบบรูปภาพ', 'รูปแบบที่อ่านได้อย่างเดียว', 'รูปแบบที่อ่านและสามารถแก้ไขได้', 'c', NULL, NULL, NULL, NULL, NULL),
(110, 24, 1, 'ตาราง Customer หมายถึงข้อใด', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'รายละเอียดการสั่งซื้อ', 'c', NULL, NULL, NULL, NULL, NULL),
(111, 24, 1, 'ตาราง Employee หมายถึงข้อใด', 'สินค้า', 'ลูกค้า', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'd', NULL, NULL, NULL, NULL, NULL),
(112, 24, 1, 'ตาราง Order Details หมายถึงข้อใด', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'a', NULL, NULL, NULL, NULL, NULL),
(113, 24, 1, 'ตาราง Products หมายถึงข้อใด', 'รายละเอียดการสั่งซื้อ', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'c', NULL, NULL, NULL, NULL, NULL),
(114, 24, 1, 'ตาราง Categories หมายถึงข้อใด', 'หมวดหมู่', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'a', NULL, NULL, NULL, NULL, NULL),
(115, 24, 1, 'ตาราง Suppliers หมายถึงข้อใด', 'พนักงาน', 'สินค้า', 'ลูกค้า', 'ผู้ขาย', 'd', NULL, NULL, NULL, NULL, NULL),
(116, 24, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 หมวดหมู่มีหลายสินค้า', '1 สินค้ามีหลายหมวดหมู่', '1 หมวดหมู่มีหลายหมวดหมู่', '1 ผู้ขายมีหลายสินค้า', 'a', 'que13.jpg', NULL, NULL, NULL, NULL),
(117, 24, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 หมวดหมู่มีหลายสินค้า', 'ลูกค้า 1 คนสามารถสั่งซื้อได้หลายครั้ง', 'ลูกค้าหลายคนสามารถซื้อได้ 1 อย่าง', '1 ผู้ขายมีหลายสินค้า', 'b', 'que14.jpg', NULL, NULL, NULL, NULL),
(118, 24, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', 'พนักงาน 1 คนมีหลายการขาย', '1 หมวดหมู่มีหลายสินค้า', '1 ผู้ขายมีหลายสินค้า', 'พนักงาน 2 คนมี 1 การขาย', 'a', 'que15.jpg', NULL, NULL, NULL, NULL),
(119, 24, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', 'พนักงาน 1 คน มีหลายการขาย', 'สินค้า 1 ชิ้น มีหลายการสั่งซื้อ', '1 หมวดหมู่มีหลายสินค้า', '1 สินค้ามีหลายหมวดหมู่', 'b', 'que16.jpg', NULL, NULL, NULL, NULL),
(120, 24, 1, 'ตามตารางจะเห็นเส้นความสัมพันธ์ ความหมายตรงกับข้อใด', '1 ผู้ขายมีพนักงาน 1 คน', '1 ผู้ขายมี 1 สินค้า', '1 สินค้ามีหลายหมวดหมู่', '1 ผู้ขายมีหลายสินค้า', 'd', 'que17.jpg', NULL, NULL, NULL, NULL),
(121, 25, 1, 'การสร้างกราฟใน Power BI สามารถใช้เครื่องมือใดได้บ้าง?', 'Chart', 'Visualization Pane', 'Data Table', 'Power Query', 'b', NULL, NULL, NULL, NULL, NULL),
(122, 25, 1, 'Data Visualization หมายถึงข้อใด', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'การจัดหน้ากระดาษ', 'การแสดงข้อมูล', 'การจัดการกับความสัมพันธ์ของตัวเลข', 'd', NULL, NULL, NULL, NULL, NULL),
(123, 25, 1, 'ฟีเจอร์ใดใน Power BI ที่ใช้สำหรับการสร้างแผนที่?', 'Map Visual', 'Line Chart', 'Pie Chart', 'Table', 'a', NULL, NULL, NULL, NULL, NULL),
(124, 25, 1, 'หากต้องการแสดงค่าต่าง ๆ ในแต่ละเซลล์ของตาราง คุณควรใช้ฟีเจอร์ใด?', 'Card', 'Matrix', 'Table', 'Gauge', 'c', NULL, NULL, NULL, NULL, NULL),
(125, 25, 1, 'หากภาพของแผนที่ไม่ปรากฎให้ทำตามขั้นตอนใด', 'ตัวเลือก>ตัวเลือกและการตั้งค่า>File >ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'ตัวเลือก> File >ตัวเลือกและการตั้งค่า>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'File>ตัวเลือกและการตั้งค่า>ตัวเลือก>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'File>ตัวเลือก>ตัวเลือกและการตั้งค่า>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'c', NULL, NULL, NULL, NULL, NULL),
(126, 25, 1, 'สัญลักษณ์นี้คือข้อใด', 'Drill Down', 'Drill Up', 'Drill Download', 'Down Up', 'a', 'que18.jpg', NULL, NULL, NULL, NULL),
(127, 25, 1, 'สัญลักษณ์นี้คือข้อใด', 'Drill Down', 'Drill Download', 'Down Up', 'Drill Up', 'd', 'que19.jpg', NULL, NULL, NULL, NULL),
(128, 25, 1, 'เลื่อนลูกกลิ้งเม้าส์เพื่ออะไร', 'เพื่อซูมเข้า-ออก', 'เพื่อความสนุก', 'เพื่อความผ่อนคลาย', 'ถูกทุกข้อ', 'a', NULL, NULL, NULL, NULL, NULL),
(129, 25, 1, 'Report View หมายถึงข้อใด', 'การเรียนรู้', 'การผ่อนคลาย', 'การสรุปและแสดงผลที่อยากรู้', 'การประมวลผล', 'c', NULL, NULL, NULL, NULL, NULL),
(130, 25, 1, 'Drill Up หมายถึงข้อใด', 'กดลูกศรขึ้น เพื่อขึ้นมา 1 Level', 'กดคลิกเม้าส์ 1 ครั้ง', 'ยืนขึ้น', 'กดลูกศรชี้ลง เพื่อลงไป 1 Level', 'a', NULL, NULL, NULL, NULL, NULL),
(131, 25, 1, 'Drill Down หมายถึงข้อใด', 'นั่งลง', 'กดลูกศรขึ้น เพื่อขึ้นมา 1 Level', 'กดลูกศรชี้ลง เพื่อลงไป 1 Level', 'การเจรจาธุรกิจ', 'c', NULL, NULL, NULL, NULL, NULL),
(132, 25, 1, 'สัญลักษณ์นี้คือข้อใด', 'จัดรูปแบบภาพ', 'จัดรูปแบบตัวอักษร', 'จัดหน้ากระดาษ', 'จัดรูปแบบแผนภูมิ', 'a', 'que20.jpg', NULL, NULL, NULL, NULL),
(133, 25, 1, 'สัญลักษณ์นี้คือข้อใด', 'เพิ่มข้อมูลลงในบรรทัด', 'Save ข้อมูล', 'เพิ่มข้อมูลลงในคีย์บอร์ด', 'เพิ่มข้อมูลลงในภาพ', 'd', 'que21.jpg', NULL, NULL, NULL, NULL),
(134, 25, 1, 'ในการสร้างกราฟที่แสดงจำนวนเปอร์เซ็นต์ของแต่ละหมวดหมู่ คุณควรใช้กราฟชนิดใด?', 'Pie Chart', 'Line Chart', 'Clustered Bar Char', 'Matrix', 'a', NULL, NULL, NULL, NULL, NULL),
(135, 25, 1, 'อะไรไม่ใช่สาเหตุหลักที่ทำให้ต้องแสดงข้อมูลเป็นภาพ', 'ความสามารถในการโน้มน้าวดึงดูดใจให้คล้อยตาม', 'ประสิทธิภาพในการรับข้อมูลและประมวลผลภาพของมนุษย์', 'การวิเคราะห์ข้อมูลเบื้องต้น', 'ความสวยงาม ตื่นตาตื่นใจ', 'd', NULL, NULL, NULL, NULL, NULL),
(136, 25, 1, 'ปัจจัยแรกที่ต้องคำนึงถึงเมื่อแสดงข้อมูลเป็นภาพคืออะไร', 'ความสวยงาม น่าติดตาม', 'ความถูกต้องของข้อมูลที่แสดงออกไป', 'ปริมาณพื้นที่ที่ใช้ในการแสดงผล', 'ความพึงพอใจของผู้แสดงข้อมูล', 'b', NULL, NULL, NULL, NULL, NULL),
(137, 25, 1, 'ข้อใดไม่ใช่สิ่งที่ต้องทำก่อนการแสดงผลข้อมูล', 'การสำรวจ', 'การทำความสะอาดข้อมูล ', 'การแปลงข้อมูลเป็นรูปแบบต่างๆ', 'การวัดผลข้อมูล', 'd', NULL, NULL, NULL, NULL, NULL),
(138, 25, 1, 'ข้อใดเป็นข้อมูลที่มีลำดับแน่นอน ', 'รายการเลขสลากกินแบ่งรัฐบาลที่ถูกรางวัลในปีที่ผ่านมา', 'อันดับความสูงของพนักงานในบริษัทหนึ่ง', 'เลขประจำตัวพนักงาน', 'รหัสไปรษณีย์ของร้านค้าแต่ละสาขา', 'a', NULL, NULL, NULL, NULL, NULL),
(139, 25, 1, 'ข้อใดเป็นข้อมูลที่ไม่มีลำดับแน่นอน', 'รายการปีอธิกสุรทิน (ปีที่มีวันที่ 29 กุมภาพันธ์ หรือ 366 วัน)', 'อุณหภูมิเฉลี่ยของแต่ละวันในกรุงเทพฯ', 'อายุพนักงานในบริษัท', 'รายชื่อพนักงานที่ทำยอดขายสูงสุด', 'b', NULL, NULL, NULL, NULL, NULL),
(140, 25, 1, 'ข้อใดต่อไปนี้เป็นแผนภูมิโดนัท (Doughnut Chart)', '', '', '', '', 'd', NULL, 'que22.jpg', 'que23.jpg', 'que24.jpg', 'que25.jpg'),
(141, 26, 1, 'การสร้างกราฟใน Power BI สามารถใช้เครื่องมือใดได้บ้าง?', 'Chart', 'Visualization Pane', 'Data Table', 'Power Query', 'b', NULL, NULL, NULL, NULL, NULL),
(142, 26, 1, 'Data Visualization หมายถึงข้อใด', 'การจัดการกับความสัมพันธ์ของข้อมูล', 'การจัดหน้ากระดาษ', 'การแสดงข้อมูล', 'การจัดการกับความสัมพันธ์ของตัวเลข', 'd', NULL, NULL, NULL, NULL, NULL),
(143, 26, 1, 'ฟีเจอร์ใดใน Power BI ที่ใช้สำหรับการสร้างแผนที่?', 'Map Visual', 'Line Chart', 'Pie Chart', 'Table', 'a', NULL, NULL, NULL, NULL, NULL),
(144, 26, 1, 'หากต้องการแสดงค่าต่าง ๆ ในแต่ละเซลล์ของตาราง คุณควรใช้ฟีเจอร์ใด?', 'Card', 'Matrix', 'Table', 'Gauge', 'c', NULL, NULL, NULL, NULL, NULL),
(145, 26, 1, 'หากภาพของแผนที่ไม่ปรากฎให้ทำตามขั้นตอนใด', 'ตัวเลือก>ตัวเลือกและการตั้งค่า>File >ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'ตัวเลือก> File >ตัวเลือกและการตั้งค่า>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'File>ตัวเลือกและการตั้งค่า>ตัวเลือก>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'File>ตัวเลือก>ตัวเลือกและการตั้งค่า>ความปลอดภัย>ติ๊กใช้ภาพแผนที่และแผนที่แถบสี>ตกลง', 'c', NULL, NULL, NULL, NULL, NULL),
(146, 26, 1, 'สัญลักษณ์นี้คือข้อใด', 'Drill Down', 'Drill Up', 'Drill Download', 'Down Up', 'a', 'que18.jpg', NULL, NULL, NULL, NULL),
(147, 26, 1, 'สัญลักษณ์นี้คือข้อใด', 'Drill Down', 'Drill Download', 'Down Up', 'Drill Up', 'd', 'que19.jpg', NULL, NULL, NULL, NULL),
(148, 26, 1, 'เลื่อนลูกกลิ้งเม้าส์เพื่ออะไร', 'เพื่อซูมเข้า-ออก', 'เพื่อความสนุก', 'เพื่อความผ่อนคลาย', 'ถูกทุกข้อ', 'a', NULL, NULL, NULL, NULL, NULL),
(149, 26, 1, 'Report View หมายถึงข้อใด', 'การเรียนรู้', 'การผ่อนคลาย', 'การสรุปและแสดงผลที่อยากรู้', 'การประมวลผล', 'c', NULL, NULL, NULL, NULL, NULL),
(150, 26, 1, 'Drill Up หมายถึงข้อใด', 'กดลูกศรขึ้น เพื่อขึ้นมา 1 Level', 'กดคลิกเม้าส์ 1 ครั้ง', 'ยืนขึ้น', 'กดลูกศรชี้ลง เพื่อลงไป 1 Level', 'a', NULL, NULL, NULL, NULL, NULL),
(151, 26, 1, 'Drill Down หมายถึงข้อใด', 'นั่งลง', 'กดลูกศรขึ้น เพื่อขึ้นมา 1 Level', 'กดลูกศรชี้ลง เพื่อลงไป 1 Level', 'การเจรจาธุรกิจ', 'c', NULL, NULL, NULL, NULL, NULL),
(152, 26, 1, 'สัญลักษณ์นี้คือข้อใด', 'จัดรูปแบบภาพ', 'จัดรูปแบบตัวอักษร', 'จัดหน้ากระดาษ', 'จัดรูปแบบแผนภูมิ', 'a', 'que20.jpg', NULL, NULL, NULL, NULL),
(153, 26, 1, 'สัญลักษณ์นี้คือข้อใด', 'เพิ่มข้อมูลลงในบรรทัด', 'Save ข้อมูล', 'เพิ่มข้อมูลลงในคีย์บอร์ด', 'เพิ่มข้อมูลลงในภาพ', 'd', 'que21.jpg', NULL, NULL, NULL, NULL),
(154, 26, 1, 'ในการสร้างกราฟที่แสดงจำนวนเปอร์เซ็นต์ของแต่ละหมวดหมู่ คุณควรใช้กราฟชนิดใด?', 'Pie Chart', 'Line Chart', 'Clustered Bar Char', 'Matrix', 'a', NULL, NULL, NULL, NULL, NULL),
(155, 26, 1, 'อะไรไม่ใช่สาเหตุหลักที่ทำให้ต้องแสดงข้อมูลเป็นภาพ', 'ความสามารถในการโน้มน้าวดึงดูดใจให้คล้อยตาม', 'ประสิทธิภาพในการรับข้อมูลและประมวลผลภาพของมนุษย์', 'การวิเคราะห์ข้อมูลเบื้องต้น', 'ความสวยงาม ตื่นตาตื่นใจ', 'd', NULL, NULL, NULL, NULL, NULL),
(156, 26, 1, 'ปัจจัยแรกที่ต้องคำนึงถึงเมื่อแสดงข้อมูลเป็นภาพคืออะไร', 'ความสวยงาม น่าติดตาม', 'ความถูกต้องของข้อมูลที่แสดงออกไป', 'ปริมาณพื้นที่ที่ใช้ในการแสดงผล', 'ความพึงพอใจของผู้แสดงข้อมูล', 'b', NULL, NULL, NULL, NULL, NULL),
(157, 26, 1, 'ข้อใดไม่ใช่สิ่งที่ต้องทำก่อนการแสดงผลข้อมูล', 'การสำรวจ', 'การทำความสะอาดข้อมูล ', 'การแปลงข้อมูลเป็นรูปแบบต่างๆ', 'การวัดผลข้อมูล', 'd', NULL, NULL, NULL, NULL, NULL),
(158, 26, 1, 'ข้อใดเป็นข้อมูลที่มีลำดับแน่นอน ', 'รายการเลขสลากกินแบ่งรัฐบาลที่ถูกรางวัลในปีที่ผ่านมา', 'อันดับความสูงของพนักงานในบริษัทหนึ่ง', 'เลขประจำตัวพนักงาน', 'รหัสไปรษณีย์ของร้านค้าแต่ละสาขา', 'a', NULL, NULL, NULL, NULL, NULL),
(159, 26, 1, 'ข้อใดเป็นข้อมูลที่ไม่มีลำดับแน่นอน', 'รายการปีอธิกสุรทิน (ปีที่มีวันที่ 29 กุมภาพันธ์ หรือ 366 วัน)', 'อุณหภูมิเฉลี่ยของแต่ละวันในกรุงเทพฯ', 'อายุพนักงานในบริษัท', 'รายชื่อพนักงานที่ทำยอดขายสูงสุด', 'b', NULL, NULL, NULL, NULL, NULL),
(160, 26, 1, 'ข้อใดต่อไปนี้เป็นแผนภูมิโดนัท (Doughnut Chart)', '', '', '', '', 'd', NULL, 'que22.jpg', 'que23.jpg', 'que24.jpg', 'que25.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

CREATE TABLE `quiz` (
  `quiz_id` int(11) NOT NULL,
  `quiz_name` varchar(100) DEFAULT NULL,
  `lesson_id` int(11) NOT NULL,
  `passing_percentage` int(11) DEFAULT NULL,
  `quiz_date` datetime DEFAULT current_timestamp(),
  `quiz_type` enum('Pre-Test','Post-Test') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`quiz_id`, `quiz_name`, `lesson_id`, `passing_percentage`, `quiz_date`, `quiz_type`) VALUES
(9, 'Pre-Test', 1, 0, '2024-06-13 22:34:34', 'Pre-Test'),
(16, 'Post-Test', 1, 70, '2024-08-15 17:45:21', 'Post-Test'),
(17, 'Pre-Test', 3, 0, '2024-06-16 16:50:31', 'Pre-Test'),
(18, 'Post-Test', 3, 70, '2024-08-15 17:45:24', 'Post-Test'),
(23, 'Pre-Test', 12, 0, '2024-07-25 20:59:03', 'Pre-Test'),
(24, 'Post-Test', 12, 70, '2024-08-15 17:45:28', 'Post-Test'),
(25, 'Pre-Test', 13, 0, '2024-07-25 20:59:27', 'Pre-Test'),
(26, 'Post-Test', 13, 70, '2024-08-15 17:45:31', 'Post-Test');

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
(1, 33, 9, 1, 8, 10, '2024-08-18 09:11:42', 1),
(2, 33, 16, 1, 8, 10, '2024-08-18 09:13:41', 1),
(3, 33, 17, 3, 3, 10, '2024-08-18 09:14:14', 1),
(4, 33, 18, 3, 8, 10, '2024-08-18 09:19:24', 1),
(5, 33, 23, 12, 9, 10, '2024-08-18 09:21:20', 1),
(6, 33, 24, 12, 10, 10, '2024-08-18 09:22:44', 1),
(7, 33, 25, 13, 4, 10, '2024-08-18 09:23:25', 1),
(8, 33, 26, 13, 6, 10, '2024-08-18 09:24:32', 0),
(9, 33, 26, 13, 7, 10, '2024-08-18 09:25:39', 1),
(10, 33, 26, 13, 7, 10, '2024-08-18 09:26:46', 1),
(11, 33, 26, 13, 7, 10, '2024-08-18 09:27:07', 1),
(12, 33, 26, 13, 9, 10, '2024-08-18 10:52:13', 1),
(13, 20, 9, 1, 7, 10, '2024-08-20 16:20:58', 1),
(14, 20, 16, 1, 9, 10, '2024-08-20 16:26:10', 1),
(15, 20, 17, 3, 6, 10, '2024-08-20 16:26:27', 1),
(16, 20, 18, 3, 9, 10, '2024-08-20 16:28:27', 1),
(17, 20, 23, 12, 2, 10, '2024-08-20 16:28:40', 1),
(18, 20, 24, 12, 10, 10, '2024-08-20 16:30:26', 1),
(19, 20, 25, 13, 1, 10, '2024-08-20 16:30:35', 1),
(20, 20, 26, 13, 10, 10, '2024-08-20 16:32:24', 1),
(21, 47, 9, 1, 9, 10, '2024-08-20 17:04:47', 1),
(23, 50, 9, 1, 7, 10, '2024-10-11 10:09:18', 1),
(24, 50, 16, 1, 8, 10, '2024-10-11 10:10:27', 1),
(25, 50, 17, 3, 3, 10, '2024-10-11 10:10:41', 1),
(26, 50, 18, 3, 7, 10, '2024-10-11 10:11:45', 1),
(27, 50, 23, 12, 2, 10, '2024-10-11 10:11:59', 1),
(28, 50, 24, 12, 7, 10, '2024-10-11 10:13:12', 1),
(29, 50, 25, 13, 4, 10, '2024-10-11 10:13:23', 1),
(30, 50, 26, 13, 8, 10, '2024-10-11 10:14:36', 1),
(31, 51, 9, 1, 4, 10, '2024-10-11 10:15:26', 1),
(32, 51, 16, 1, 9, 10, '2024-10-11 10:16:39', 1),
(33, 51, 17, 3, 3, 10, '2024-10-11 10:16:50', 1),
(34, 51, 18, 3, 5, 10, '2024-10-11 10:17:59', 0),
(35, 51, 18, 3, 8, 10, '2024-10-11 10:19:23', 1),
(36, 51, 23, 12, 1, 10, '2024-10-11 10:19:35', 1),
(37, 51, 24, 12, 6, 10, '2024-10-11 10:21:01', 0),
(38, 51, 24, 12, 6, 10, '2024-10-11 10:22:05', 0),
(39, 51, 24, 12, 8, 10, '2024-10-11 10:22:42', 1),
(40, 51, 25, 13, 2, 10, '2024-10-11 10:22:52', 1),
(41, 51, 26, 13, 7, 10, '2024-10-11 10:23:57', 1),
(42, 51, 26, 13, 7, 10, '2024-10-11 10:25:18', 1),
(43, 50, 26, 13, 7, 10, '2024-10-11 10:30:29', 1),
(44, 48, 9, 1, 10, 10, '2024-10-11 13:56:23', 1),
(45, 48, 16, 1, 9, 10, '2024-10-11 14:29:01', 1),
(46, 48, 17, 3, 3, 10, '2024-10-11 14:29:15', 1),
(47, 48, 18, 3, 8, 10, '2024-10-11 14:30:03', 1),
(48, 48, 23, 12, 3, 10, '2024-10-11 14:30:21', 1),
(49, 48, 24, 12, 9, 10, '2024-10-11 14:32:40', 1),
(50, 48, 25, 13, 2, 10, '2024-10-11 14:32:51', 1),
(51, 48, 26, 13, 9, 10, '2024-10-11 14:33:43', 1);

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
(47, '-', '-', '-', '-', 0, '-', 9, 1),
(48, 'Turn Data To Insigth With Power BI', 'NXfiYp1BHpE', 'ในรายวิชา \"เริ่มต้น Power BI\" ผู้เรียนจะได้เรียนรู้พื้นฐานและการใช้งานโปรแกรม Power BI ซึ่งเป็นเครื่องมือที่ทรงพลังสำหรับการวิเคราะห์และแสดงผลข้อมูล รายวิชานี้จะครอบคลุมเนื้อหาตั้งแต่การนำเข้าข้อมูลจากแหล่งต่างๆ การสร้างและปรับแต่งแผนภูมิและแดชบอร์ด การตั้งค่าตัวกรอง และการสร้างรายงานที่มีประสิทธิภาพ', '5', 0, '../static/img/updated/video_img/Turn_data.jpg', NULL, 1),
(49, '-', '-', '-', '-', 0, '-', 16, 1),
(50, '-', '-', '-', '-', 0, '-', 17, 3),
(51, 'การแปลงข้อมูลด้วย Power BI', 'zvJG_UkcRNU', '\"การแปลงข้อมูลด้วย Power BI\" เน้นการเรียนรู้ทักษะและเทคนิคในการแปลงข้อมูล (Data Transformation) เพื่อเตรียมข้อมูลให้พร้อมสำหรับการวิเคราะห์และแสดงผลอย่างมีประสิทธิภาพใน Power BI ผู้เรียนจะได้ทำความเข้าใจกระบวนการตั้งแต่การนำเข้าข้อมูล การทำความสะอาดข้อมูล (Data Cleaning) การรวมข้อมูลจากแหล่งข้อมูลหลาย ๆ แหล่ง การสร้างคอลัมน์คำนวณ และการสร้างความสัมพันธ์ระหว่างตารางข้อมูลต่าง ๆ', '8', 0, '../static/img/updated/video_img/Data_transformation.jpg', NULL, 3),
(52, '-', '-', '-', '-', 0, '-', 18, 3),
(56, '-', '-', '-', '-', 0, '-', 23, 12),
(57, 'ความสัมพันธ์', 'yLRRSHL1EyA', 'วิดีโอนี้จะพูดถึง \"ความสัมพันธ์\" ใน Power BI ซึ่งเป็นคุณสมบัติที่สำคัญในการจัดการข้อมูลและสร้างรายงานที่มีประสิทธิภาพ. ความสัมพันธ์ (Relationships)  ช่วยให้คุณสามารถเชื่อมโยงตารางข้อมูลต่างๆ ได้อย่างมีประสิทธิภาพเพื่อให้ข้อมูลในรายงานของคุณมีความแม่นยำและสมบูรณ์. โดยหลักการแล้ว, ความสัมพันธ์ใน Power BI สามารถทำได้ทั้งแบบ One-to-Many, Many-to-One, และ Many-to-Many ซึ่งแต่ละประเภทมีลักษณะการใช้งานและวิธีการสร้างที่แตกต่างกัน. เรียนรู้วิธีการสร้างและจัดการความสัมพันธ์ใน Power BI จะช่วยให้คุณสามารถทำงานกับข้อมูลที่ซับซ้อนได้ง่ายขึ้น และทำให้การสร้างรายงานและการวิเคราะห์ข้อมูลเป็นไปอย่างราบรื่น.', '12', 0, '../static/img/updated/video_img/Relationship.png', NULL, 12),
(58, '-', '-', '-', '-', 0, '-', 24, 12),
(59, '-', '-', '-', '-', 0, '-', 25, 13),
(60, 'Data Visualization ใน Power BI', 'k3jSxhHQo6g', 'วิดีโอนี้สำรวจหัวข้อ \"Data Visualization\" หรือการสร้างการแสดงผลข้อมูลใน Power BI ซึ่งเป็นเครื่องมือที่มีความสามารถในการแสดงผลข้อมูลที่มีความหลากหลาย การแสดงผลข้อมูล (Data Visualization) ช่วยให้คุณสามารถสื่อสารข้อมูลที่ซับซ้อนได้อย่างชัดเจนและเข้าใจง่าย. Power BI มีเครื่องมือและฟีเจอร์ต่างๆ สำหรับการสร้างกราฟ, แผนภูมิ, และการแสดงผลข้อมูลแบบอื่นๆ ที่ช่วยให้คุณสามารถวิเคราะห์และนำเสนอข้อมูลได้อย่างมีประสิทธิภาพ. เราจะพูดถึงวิธีการใช้เครื่องมือต่างๆ เช่น Bar Charts, Line Charts, Pie Charts และการใช้งาน Dashboard เพื่อให้คุณสามารถเลือกวิธีการแสดงผลที่เหมาะสมกับข้อมูลของคุณได้.', '7', 0, '../static/img/updated/video_img/Data_visualization.png', NULL, 13),
(61, '-', '-', '-', '-', 0, '-', 26, 13);

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
  `registration_date` datetime NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(60) NOT NULL,
  `role` enum('user') NOT NULL DEFAULT 'user',
  `userimage` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `last_name`, `username`, `email`, `registration_date`, `password`, `gender`, `role`, `userimage`) VALUES
(20, 'ปิยะ', 'กุลมี', 'bank123', 'bank@gmail.com', '2024-05-27 00:00:00', 'Bank1234', 'Male', 'user', '../static/img/updated/user/bank.jpg'),
(33, 'Chutmongkol', 'Sangsakul', 'jame111', 'jame@gmail.com', '2024-05-29 23:03:33', 'Jame1234', 'Male', 'user', '../static/img/updated/user/jame.jpg'),
(47, 'Kanthavee', 'Phongsarai', 'mon1', 'mon@gmail.com', '2024-08-18 16:03:32', 'Mon12345', 'Male', 'user', '../static/img/uploads/users/mon.jpg'),
(48, 'Natthaphat', 'Pankaing', 'Oat005', 'oat123@gmail.com', '2024-08-18 18:02:10', 'Oat12345', 'Male', 'user', '../static/img/updated/user/oat.jpg'),
(50, 'Tamonpun', 'Intawong', 'Ploy019', 'ploy123@gmail.com', '2024-10-11 17:04:28', 'Ploy1234', 'Female', 'user', '../static/img/uploads/users/ploy.jpg'),
(51, 'Nuchanart', 'Tientong', 'Puy007', 'puy123@gmail.com', '2024-10-11 17:06:23', 'Puy12345', 'Female', 'user', '../static/img/uploads/users/puy.jpg');

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

INSERT INTO `user_enroll` (`enroll_id`, `user_id`, `course_id`, `enroll_date`, `is_completed`, `completed_at`) VALUES
(1, 33, 4, '2024-08-18 16:11:02', 1, '2024-08-18 10:52:13'),
(2, 20, 4, '2024-08-20 23:19:06', 1, '2024-08-20 16:32:24'),
(3, 47, 4, '2024-08-21 00:02:14', 0, NULL),
(5, 50, 4, '2024-10-11 17:08:35', 1, '2024-10-11 10:30:29'),
(6, 51, 4, '2024-10-11 17:15:11', 1, '2024-10-11 10:25:18'),
(7, 48, 4, '2024-10-11 20:42:54', 1, '2024-10-11 14:33:43');

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
  `passed` tinyint(1) NOT NULL,
  `watched_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `video_attempts`
--

INSERT INTO `video_attempts` (`attempt_id`, `user_id`, `video_id`, `lesson_id`, `attempt_date`, `passed`, `watched_at`) VALUES
(1, 33, 48, 1, '2024-08-18 16:11:44', 1, '2024-08-18 10:48:12'),
(2, 33, 51, 3, '2024-08-18 16:14:15', 1, '2024-08-18 09:14:26'),
(3, 33, 57, 12, '2024-08-18 16:21:22', 1, '2024-08-18 09:21:35'),
(4, 33, 60, 13, '2024-08-18 16:23:26', 1, '2024-08-18 09:23:37'),
(5, 20, 48, 1, '2024-08-20 23:21:00', 1, '2024-08-20 16:21:58'),
(6, 20, 51, 3, '2024-08-20 23:26:28', 1, '2024-08-20 16:26:41'),
(7, 20, 57, 12, '2024-08-20 23:28:41', 1, '2024-08-20 16:29:04'),
(8, 20, 60, 13, '2024-08-20 23:30:37', 1, '2024-08-20 16:30:50'),
(21, 47, 48, 1, '2024-08-21 00:04:49', 0, '2024-08-20 17:05:18'),
(24, 50, 48, 1, '2024-10-11 17:09:20', 1, '2024-10-11 10:09:32'),
(25, 50, 51, 3, '2024-10-11 17:10:42', 1, '2024-10-11 10:10:50'),
(26, 50, 57, 12, '2024-10-11 17:12:00', 1, '2024-10-11 10:12:07'),
(27, 50, 60, 13, '2024-10-11 17:13:25', 1, '2024-10-11 10:13:29'),
(28, 51, 48, 1, '2024-10-11 17:15:27', 1, '2024-10-11 10:15:38'),
(29, 51, 51, 3, '2024-10-11 17:16:51', 1, '2024-10-11 10:16:56'),
(30, 51, 57, 12, '2024-10-11 17:19:36', 1, '2024-10-11 10:19:42'),
(31, 51, 60, 13, '2024-10-11 17:22:53', 1, '2024-10-11 10:22:59'),
(32, 48, 48, 1, '2024-10-11 20:58:53', 1, '2024-10-11 14:28:18'),
(33, 48, 51, 3, '2024-10-11 21:29:16', 1, '2024-10-11 14:29:25'),
(34, 48, 57, 12, '2024-10-11 21:30:23', 1, '2024-10-11 14:30:31'),
(35, 48, 60, 13, '2024-10-11 21:32:53', 1, '2024-10-11 14:33:03');

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
  ADD KEY `lesson_ibfk_1` (`course_id`),
  ADD KEY `lesson_ibfk_2` (`instructor_id`);

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
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `lesson`
--
ALTER TABLE `lesson`
  MODIFY `lesson_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `question`
--
ALTER TABLE `question`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=162;

--
-- AUTO_INCREMENT for table `quiz`
--
ALTER TABLE `quiz`
  MODIFY `quiz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `quiz_attempts`
--
ALTER TABLE `quiz_attempts`
  MODIFY `attempt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `quiz_video`
--
ALTER TABLE `quiz_video`
  MODIFY `video_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `user_enroll`
--
ALTER TABLE `user_enroll`
  MODIFY `enroll_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `video_attempts`
--
ALTER TABLE `video_attempts`
  MODIFY `attempt_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

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
  ADD CONSTRAINT `lesson_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `lesson_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`id`);

--
-- Constraints for table `question`
--
ALTER TABLE `question`
  ADD CONSTRAINT `question_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`quiz_id`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `video_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `video_attempts_ibfk_2` FOREIGN KEY (`video_id`) REFERENCES `quiz_video` (`video_id`),
  ADD CONSTRAINT `video_attempts_ibfk_3` FOREIGN KEY (`lesson_id`) REFERENCES `lesson` (`lesson_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
