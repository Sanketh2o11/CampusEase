-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: campusease
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_batch`
--

DROP TABLE IF EXISTS `accounts_batch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_batch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `year` int NOT NULL,
  `department` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_batch`
--

LOCK TABLES `accounts_batch` WRITE;
/*!40000 ALTER TABLE `accounts_batch` DISABLE KEYS */;
INSERT INTO `accounts_batch` VALUES (1,'CS2024',2024,'CS'),(2,'CS-2023',2023,'Computer Science');
/*!40000 ALTER TABLE `accounts_batch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `role` varchar(10) NOT NULL,
  `batch_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `accounts_user_batch_id_02df8cc1_fk_accounts_batch_id` (`batch_id`),
  CONSTRAINT `accounts_user_batch_id_02df8cc1_fk_accounts_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `accounts_batch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$1000000$Elypunb7HkbdVdgcNkY1Za$bIETmD86lFH9YRyhYjx3xiajvX1f34b5LrP0tcC+RYs=','2026-03-16 10:30:11.016933',1,'','',1,1,'2026-03-16 10:09:39.385842','superuser@campusease.com','','cr',NULL),(2,'pbkdf2_sha256$1000000$nnnBIENibO28QVASUErie4$KkBCRPFVUIy/ksUHOkkBIQc8OEIe0MrIIIL8z/G4Dj8=','2026-03-19 06:57:38.725140',0,'','',0,1,'2026-03-19 06:57:35.757483','testuser@example.com','Test User','student',NULL),(3,'pbkdf2_sha256$1000000$xcXRQw3xec9fBSvw2oBRrg$UG53AmY1JqZyiLi/dwJs68rXUXgs+R5wVM+f6AUN7ds=','2026-03-19 07:01:42.632608',0,'','',0,1,'2026-03-19 07:01:38.774178','test2@test.com','Finder User','student',NULL),(4,'pbkdf2_sha256$1000000$rouHZzDjyrJNp9fl3r3J4j$LeC0ErfUKU9/zddpaX3xbto9o1Uxz4cd2eufjb7mE9k=','2026-03-19 08:31:20.121422',0,'','',0,1,'2026-03-19 08:23:04.276247','cr@test.com','Test CR','cr',1),(5,'pbkdf2_sha256$1000000$FWzBtA0P9COeIWyp69NAch$zI+IBQF2j7cU1I4XXV1cD2lNFLsNRyxRgvGe967lxdU=',NULL,0,'','',0,1,'2026-03-19 08:23:05.211374','student@test.com','Test Student','student',1),(6,'pbkdf2_sha256$1000000$C2VBN1mWHWjhYFgqvTslIu$FrBIutKfDTxclr0ck34CXtuscPTfg3wFJisBRPZzhLw=','2026-04-07 12:17:17.710235',0,'','',0,1,'2026-04-07 12:17:16.489153','sanketh.22ai900@sode-edu.in','Sank','student',1),(7,'pbkdf2_sha256$1000000$02ryugIQYVbgvu5SvcJhcO$GJJrOTP2k5aG893HyXlSht/s3XeU5f4HajiXuKacnKc=','2026-04-07 12:47:05.299574',0,'','',0,1,'2026-04-07 12:35:13.620599','cr@campusease.com','Alex Johnson','cr',2),(8,'pbkdf2_sha256$1000000$IhLScWsqSjdHdxEc7Puu8t$YMgKsjfRcXGGdDDoKLepgOcx0P0xb08GZfHEKHKZh5g=','2026-04-07 13:13:33.018664',0,'','',0,1,'2026-04-07 12:35:14.972504','student1@campusease.com','Priya Sharma','student',2),(9,'pbkdf2_sha256$1000000$D2v3O5M4qhnNFtvXnLlbpA$IY5SA48gxla1VUeCaV/i2m+UrXI2G32C/Q2Lrgk6Qx4=',NULL,0,'','',0,1,'2026-04-07 12:35:16.307394','student2@campusease.com','Rahul Verma','student',2),(10,'pbkdf2_sha256$1000000$4wEzG7GKgGz5ScVBdRn4c5$qnWYOHP6bmRJ8ImzWYb2g7eZSLAtQVuXI25ioovRRGo=',NULL,0,'','',0,1,'2026-04-07 12:35:17.702572','student3@campusease.com','Sneha Patel','student',2);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_attendance`
--

DROP TABLE IF EXISTS `attendance_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(200) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `attendance_attendance_student_id_subject_c9928c84_uniq` (`student_id`,`subject`),
  CONSTRAINT `attendance_attendance_student_id_94863613_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_attendance`
--

LOCK TABLES `attendance_attendance` WRITE;
/*!40000 ALTER TABLE `attendance_attendance` DISABLE KEYS */;
INSERT INTO `attendance_attendance` VALUES (1,'Math','2026-03-19 06:58:30.449215',2),(2,'DBMS','2026-03-19 08:36:02.668927',4),(3,'BCS714C','2026-04-07 12:40:04.643731',8),(4,'BAI755X','2026-04-07 12:40:04.643731',8),(5,'BAI702(LAB)','2026-04-07 12:40:04.643731',8),(6,'BAI701','2026-04-07 12:40:04.643731',8),(7,'BAD703','2026-04-07 12:40:04.643731',8),(8,'BAI702','2026-04-07 12:40:04.643731',8),(9,'BCS714C','2026-04-07 12:40:04.643731',9),(10,'BAI755X','2026-04-07 12:40:04.643731',9),(11,'BAI702(LAB)','2026-04-07 12:40:04.643731',9),(12,'BAI701','2026-04-07 12:40:04.643731',9),(13,'BAD703','2026-04-07 12:40:04.643731',9),(14,'BAI702','2026-04-07 12:40:04.643731',9),(15,'BCS714C','2026-04-07 12:40:04.643731',10),(16,'BAI755X','2026-04-07 12:40:04.643731',10),(17,'BAI702(LAB)','2026-04-07 12:40:04.643731',10),(18,'BAI701','2026-04-07 12:40:04.643731',10),(19,'BAD703','2026-04-07 12:40:04.643731',10),(20,'BAI702','2026-04-07 12:40:04.643731',10),(21,'BCS714C','2026-04-07 12:46:16.322920',7),(22,'BAI755X','2026-04-07 12:46:16.329930',7),(23,'BAI702(LAB)','2026-04-07 12:46:16.335933',7),(24,'BAI701','2026-04-07 12:46:16.342464',7),(25,'BAI702','2026-04-07 12:46:16.348465',7),(26,'BAD703','2026-04-07 12:46:16.354465',7);
/*!40000 ALTER TABLE `attendance_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance_attendancerecord`
--

DROP TABLE IF EXISTS `attendance_attendancerecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance_attendancerecord` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `status` varchar(12) NOT NULL DEFAULT 'not_marked',
  `student_id` bigint NOT NULL,
  `subject_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ar` (`student_id`,`subject_id`,`date`),
  KEY `fk_ar_subject` (`subject_id`),
  CONSTRAINT `fk_ar_student` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ar_subject` FOREIGN KEY (`subject_id`) REFERENCES `attendance_attendance` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance_attendancerecord`
--

LOCK TABLES `attendance_attendancerecord` WRITE;
/*!40000 ALTER TABLE `attendance_attendancerecord` DISABLE KEYS */;
INSERT INTO `attendance_attendancerecord` VALUES (1,'2026-04-07','present',8,7),(2,'2026-04-07','absent',8,6),(3,'2026-04-07','present',8,8),(4,'2026-04-07','present',8,5),(5,'2026-04-07','present',8,4);
/*!40000 ALTER TABLE `attendance_attendancerecord` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add batch',6,'add_batch'),(22,'Can change batch',6,'change_batch'),(23,'Can delete batch',6,'delete_batch'),(24,'Can view batch',6,'view_batch'),(25,'Can add user',7,'add_user'),(26,'Can change user',7,'change_user'),(27,'Can delete user',7,'delete_user'),(28,'Can view user',7,'view_user'),(29,'Can add attendance',8,'add_attendance'),(30,'Can change attendance',8,'change_attendance'),(31,'Can delete attendance',8,'delete_attendance'),(32,'Can view attendance',8,'view_attendance'),(33,'Can add notice',9,'add_notice'),(34,'Can change notice',9,'change_notice'),(35,'Can delete notice',9,'delete_notice'),(36,'Can view notice',9,'view_notice'),(37,'Can add material',10,'add_material'),(38,'Can change material',10,'change_material'),(39,'Can delete material',10,'delete_material'),(40,'Can view material',10,'view_material'),(41,'Can add exam',11,'add_exam'),(42,'Can change exam',11,'change_exam'),(43,'Can delete exam',11,'delete_exam'),(44,'Can view exam',11,'view_exam'),(45,'Can add lost found item',12,'add_lostfounditem'),(46,'Can change lost found item',12,'change_lostfounditem'),(47,'Can delete lost found item',12,'delete_lostfounditem'),(48,'Can view lost found item',12,'view_lostfounditem'),(49,'Can add timetable slot',13,'add_timetableslot'),(50,'Can change timetable slot',13,'change_timetableslot'),(51,'Can delete timetable slot',13,'delete_timetableslot'),(52,'Can view timetable slot',13,'view_timetableslot'),(53,'Can add attendance record',14,'add_attendancerecord'),(54,'Can change attendance record',14,'change_attendancerecord'),(55,'Can delete attendance record',14,'delete_attendancerecord'),(56,'Can view attendance record',14,'view_attendancerecord'),(57,'Can add poll vote',15,'add_pollvote'),(58,'Can change poll vote',15,'change_pollvote'),(59,'Can delete poll vote',15,'delete_pollvote'),(60,'Can view poll vote',15,'view_pollvote'),(61,'Can add notice poll',16,'add_noticepoll'),(62,'Can change notice poll',16,'change_noticepoll'),(63,'Can delete notice poll',16,'delete_noticepoll'),(64,'Can view notice poll',16,'view_noticepoll'),(65,'Can add notice read',17,'add_noticeread'),(66,'Can change notice read',17,'change_noticeread'),(67,'Can delete notice read',17,'delete_noticeread'),(68,'Can view notice read',17,'view_noticeread'),(69,'Can add material thank you',18,'add_materialthankyou'),(70,'Can change material thank you',18,'change_materialthankyou'),(71,'Can delete material thank you',18,'delete_materialthankyou'),(72,'Can view material thank you',18,'view_materialthankyou'),(73,'Can add batch exam',19,'add_batchexam'),(74,'Can change batch exam',19,'change_batchexam'),(75,'Can delete batch exam',19,'delete_batchexam'),(76,'Can view batch exam',19,'view_batchexam'),(77,'Can add personal exam result',20,'add_personalexamresult'),(78,'Can change personal exam result',20,'change_personalexamresult'),(79,'Can delete personal exam result',20,'delete_personalexamresult'),(80,'Can view personal exam result',20,'view_personalexamresult');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','batch'),(7,'accounts','user'),(1,'admin','logentry'),(8,'attendance','attendance'),(14,'attendance','attendancerecord'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(19,'exams','batchexam'),(11,'exams','exam'),(20,'exams','personalexamresult'),(12,'lostfound','lostfounditem'),(10,'materials','material'),(18,'materials','materialthankyou'),(9,'notices','notice'),(16,'notices','noticepoll'),(17,'notices','noticeread'),(15,'notices','pollvote'),(5,'sessions','session'),(13,'timetable','timetableslot');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-16 10:07:50.855565'),(2,'contenttypes','0002_remove_content_type_name','2026-03-16 10:07:51.012173'),(3,'auth','0001_initial','2026-03-16 10:07:51.579037'),(4,'auth','0002_alter_permission_name_max_length','2026-03-16 10:07:51.688185'),(5,'auth','0003_alter_user_email_max_length','2026-03-16 10:07:51.708451'),(6,'auth','0004_alter_user_username_opts','2026-03-16 10:07:51.725885'),(7,'auth','0005_alter_user_last_login_null','2026-03-16 10:07:51.741522'),(8,'auth','0006_require_contenttypes_0002','2026-03-16 10:07:51.749108'),(9,'auth','0007_alter_validators_add_error_messages','2026-03-16 10:07:51.764753'),(10,'auth','0008_alter_user_username_max_length','2026-03-16 10:07:51.780851'),(11,'auth','0009_alter_user_last_name_max_length','2026-03-16 10:07:51.799955'),(12,'auth','0010_alter_group_name_max_length','2026-03-16 10:07:51.837159'),(13,'auth','0011_update_proxy_permissions','2026-03-16 10:07:51.852920'),(14,'auth','0012_alter_user_first_name_max_length','2026-03-16 10:07:51.869353'),(15,'accounts','0001_initial','2026-03-16 10:07:52.655709'),(16,'admin','0001_initial','2026-03-16 10:07:52.938122'),(17,'admin','0002_logentry_remove_auto_add','2026-03-16 10:07:52.961988'),(18,'admin','0003_logentry_add_action_flag_choices','2026-03-16 10:07:52.981141'),(19,'attendance','0001_initial','2026-03-16 10:07:53.173657'),(20,'exams','0001_initial','2026-03-16 10:07:53.344542'),(21,'lostfound','0001_initial','2026-03-16 10:07:53.498008'),(22,'materials','0001_initial','2026-03-16 10:07:53.683091'),(23,'notices','0001_initial','2026-03-16 10:07:53.873224'),(24,'sessions','0001_initial','2026-03-16 10:07:53.936158'),(25,'notices','0002_notice_image_url_notice_video_url','2026-03-19 08:12:30.948862'),(26,'timetable','0001_initial','2026-04-07 03:43:04.592734');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6opyz2d1jby1hdxy1eokkne33bj89ycu','.eJxVjMsOwiAQRf-FtSGVRxlcuvcbyMAwUjWQlHZl_HfbpAvd3nPOfYuA61LC2vMcJhIXAeL0u0VMz1x3QA-s9yZTq8s8Rbkr8qBd3hrl1_Vw_w4K9rLVlvTITBgNW1LOOG8NmJHUkJJWPjJEQBz0RgEdegSrmS2crUfnTBKfL_b7OCU:1wA6FJ:7fTf-EPRDhZHPEUiYpiMChtkdDgAdu8f5y4e66TUW_k','2026-04-21 13:13:33.023674'),('6zah5svrpemsqwvpvdep8z7ccttdwvdf','.eJxVjMsOwiAUBf-FtSGAlIdL934DuQ-QqqFJaVfGf7dNutDtzJzzFgnWpaa15zmNLC7CitMvQ6BnbrvgB7T7JGlqyzyi3BN52C5vE-fX9Wj_Dir0uq0dBVJu8ECFNZuIHDxqIlWCguJU5hI0B2uyhmiiPUeDGMqGBu2pRPH5AgJFOHI:1w38mm:V5daO9eEw8BjAHNxIyNiupTAjl6ZWndb4c4cG1c2rDc','2026-04-02 08:31:20.126108'),('rxw5qc5efkmneoc30dvo64c61ah157ba','.eJxVjEEOwiAQRe_C2hCG4nTq0n3P0AwwSNVAUtqV8e7apAvd_vfef6mJtzVPW5NlmqO6qE6dfjfP4SFlB_HO5VZ1qGVdZq93RR-06bFGeV4P9-8gc8vfWsjblChgSsaiFXYIQGyJvGdHZ-swBR5MHzsQQIvGDYF6F5gTiAP1_gDsqTfR:1w37O2:9n2EW0sJl_ejhjssgBqEOtxGqM-QhsFzk4RyuKe_Y44','2026-04-02 07:01:42.643517');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exams_batchexam`
--

DROP TABLE IF EXISTS `exams_batchexam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exams_batchexam` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject` varchar(100) NOT NULL,
  `exam_name` varchar(200) NOT NULL,
  `exam_type` varchar(20) NOT NULL,
  `exam_date` date NOT NULL,
  `syllabus` longtext NOT NULL,
  `batch_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_batchexam_batch` (`batch_id`),
  KEY `fk_batchexam_creator` (`created_by_id`),
  CONSTRAINT `fk_batchexam_batch` FOREIGN KEY (`batch_id`) REFERENCES `accounts_batch` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_batchexam_creator` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exams_batchexam`
--

LOCK TABLES `exams_batchexam` WRITE;
/*!40000 ALTER TABLE `exams_batchexam` DISABLE KEYS */;
INSERT INTO `exams_batchexam` VALUES (1,'Machine Learning 2','IA-1','internal','2026-04-15','',2,7);
/*!40000 ALTER TABLE `exams_batchexam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exams_exam`
--

DROP TABLE IF EXISTS `exams_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exams_exam` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `exam_type` varchar(10) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `exam_date` date NOT NULL,
  `result_notes` longtext NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exams_exam_student_id_0f6d177b_fk_accounts_user_id` (`student_id`),
  CONSTRAINT `exams_exam_student_id_0f6d177b_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exams_exam`
--

LOCK TABLES `exams_exam` WRITE;
/*!40000 ALTER TABLE `exams_exam` DISABLE KEYS */;
INSERT INTO `exams_exam` VALUES (1,'internal','DBMS','2026-03-27','8 grade points',4);
/*!40000 ALTER TABLE `exams_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exams_personalexamresult`
--

DROP TABLE IF EXISTS `exams_personalexamresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exams_personalexamresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `score` varchar(20) NOT NULL DEFAULT '',
  `notes` longtext NOT NULL,
  `batch_exam_id` bigint DEFAULT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_per` (`student_id`,`batch_exam_id`),
  KEY `fk_per_batchexam` (`batch_exam_id`),
  CONSTRAINT `fk_per_batchexam` FOREIGN KEY (`batch_exam_id`) REFERENCES `exams_batchexam` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_per_student` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exams_personalexamresult`
--

LOCK TABLES `exams_personalexamresult` WRITE;
/*!40000 ALTER TABLE `exams_personalexamresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `exams_personalexamresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lostfound_lostfounditem`
--

DROP TABLE IF EXISTS `lostfound_lostfounditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lostfound_lostfounditem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `is_resolved` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `reporter_id` bigint NOT NULL,
  `contact_info` varchar(200) NOT NULL DEFAULT '',
  `last_seen_location` varchar(200) NOT NULL DEFAULT '',
  `claimed_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `lostfound_lostfounditem_reporter_id_a26daa50_fk_accounts_user_id` (`reporter_id`),
  KEY `fk_lf_claimed` (`claimed_by_id`),
  CONSTRAINT `fk_lf_claimed` FOREIGN KEY (`claimed_by_id`) REFERENCES `accounts_user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `lostfound_lostfounditem_reporter_id_a26daa50_fk_accounts_user_id` FOREIGN KEY (`reporter_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lostfound_lostfounditem`
--

LOCK TABLES `lostfound_lostfounditem` WRITE;
/*!40000 ALTER TABLE `lostfound_lostfounditem` DISABLE KEYS */;
INSERT INTO `lostfound_lostfounditem` VALUES (1,'Wallet','Black leather, lost in library.',NULL,'found',1,'2026-03-19 07:01:00.428314',2,'','',NULL),(2,'S','S',NULL,'lost',1,'2026-03-19 07:12:03.174090',3,'','',NULL);
/*!40000 ALTER TABLE `lostfound_lostfounditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials_material`
--

DROP TABLE IF EXISTS `materials_material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials_material` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `drive_link` varchar(500) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `uploader_id` bigint DEFAULT NULL,
  `material_type` varchar(20) NOT NULL DEFAULT 'other',
  `is_pinned` tinyint(1) NOT NULL DEFAULT '0',
  `thank_you_count` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `materials_material_uploader_id_2ae065db_fk_accounts_user_id` (`uploader_id`),
  CONSTRAINT `materials_material_uploader_id_2ae065db_fk_accounts_user_id` FOREIGN KEY (`uploader_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials_material`
--

LOCK TABLES `materials_material` WRITE;
/*!40000 ALTER TABLE `materials_material` DISABLE KEYS */;
INSERT INTO `materials_material` VALUES (1,'Design Patterns','Software Engineering','https://drive.google.com/file/d/123/view','2026-03-19 07:00:00.553138',2,'other',0,3);
/*!40000 ALTER TABLE `materials_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials_materialthankyou`
--

DROP TABLE IF EXISTS `materials_materialthankyou`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials_materialthankyou` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `material_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_mty` (`material_id`,`student_id`),
  KEY `fk_mty_student` (`student_id`),
  CONSTRAINT `fk_mty_material` FOREIGN KEY (`material_id`) REFERENCES `materials_material` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_mty_student` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials_materialthankyou`
--

LOCK TABLES `materials_materialthankyou` WRITE;
/*!40000 ALTER TABLE `materials_materialthankyou` DISABLE KEYS */;
INSERT INTO `materials_materialthankyou` VALUES (1,1,6),(2,1,7),(3,1,8);
/*!40000 ALTER TABLE `materials_materialthankyou` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notices_notice`
--

DROP TABLE IF EXISTS `notices_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notices_notice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `deadline` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `video_url` varchar(200) DEFAULT NULL,
  `notice_type` varchar(20) NOT NULL DEFAULT 'general',
  `is_pinned` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `notices_notice_author_id_99ebb3e0_fk_accounts_user_id` (`author_id`),
  CONSTRAINT `notices_notice_author_id_99ebb3e0_fk_accounts_user_id` FOREIGN KEY (`author_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notices_notice`
--

LOCK TABLES `notices_notice` WRITE;
/*!40000 ALTER TABLE `notices_notice` DISABLE KEYS */;
INSERT INTO `notices_notice` VALUES (1,'Varnothsava 2026','Its back','2026-03-18 16:04:00.000000','2026-03-16 10:35:01.260726',1,NULL,NULL,'general',0);
/*!40000 ALTER TABLE `notices_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notices_noticepoll`
--

DROP TABLE IF EXISTS `notices_noticepoll`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notices_noticepoll` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(200) NOT NULL,
  `option_yes` varchar(100) NOT NULL DEFAULT 'Yes, I''m in',
  `option_no` varchar(100) NOT NULL DEFAULT 'No, I''ll skip',
  `option_maybe` varchar(100) NOT NULL DEFAULT 'Maybe',
  `notice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `notice_id` (`notice_id`),
  CONSTRAINT `fk_noticepoll_notice` FOREIGN KEY (`notice_id`) REFERENCES `notices_notice` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notices_noticepoll`
--

LOCK TABLES `notices_noticepoll` WRITE;
/*!40000 ALTER TABLE `notices_noticepoll` DISABLE KEYS */;
/*!40000 ALTER TABLE `notices_noticepoll` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notices_noticeread`
--

DROP TABLE IF EXISTS `notices_noticeread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notices_noticeread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `read_at` datetime(6) NOT NULL,
  `notice_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_noticeread` (`notice_id`,`student_id`),
  KEY `fk_noticeread_student` (`student_id`),
  CONSTRAINT `fk_noticeread_notice` FOREIGN KEY (`notice_id`) REFERENCES `notices_notice` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_noticeread_student` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notices_noticeread`
--

LOCK TABLES `notices_noticeread` WRITE;
/*!40000 ALTER TABLE `notices_noticeread` DISABLE KEYS */;
INSERT INTO `notices_noticeread` VALUES (1,'2026-04-07 12:31:40.685083',1,6),(3,'2026-04-07 12:40:19.250730',1,7),(5,'2026-04-07 13:21:42.619766',1,8);
/*!40000 ALTER TABLE `notices_noticeread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notices_pollvote`
--

DROP TABLE IF EXISTS `notices_pollvote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notices_pollvote` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `choice` varchar(10) NOT NULL,
  `poll_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_pollvote` (`poll_id`,`student_id`),
  KEY `fk_pollvote_student` (`student_id`),
  CONSTRAINT `fk_pollvote_poll` FOREIGN KEY (`poll_id`) REFERENCES `notices_noticepoll` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_pollvote_student` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notices_pollvote`
--

LOCK TABLES `notices_pollvote` WRITE;
/*!40000 ALTER TABLE `notices_pollvote` DISABLE KEYS */;
/*!40000 ALTER TABLE `notices_pollvote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable_timetableslot`
--

DROP TABLE IF EXISTS `timetable_timetableslot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable_timetableslot` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `day` varchar(10) NOT NULL,
  `period` int NOT NULL,
  `subject_name` varchar(100) NOT NULL,
  `batch_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timetable_timetableslot_batch_id_day_period_7c1e0b30_uniq` (`batch_id`,`day`,`period`),
  CONSTRAINT `timetable_timetableslot_batch_id_c750f57a_fk_accounts_batch_id` FOREIGN KEY (`batch_id`) REFERENCES `accounts_batch` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable_timetableslot`
--

LOCK TABLES `timetable_timetableslot` WRITE;
/*!40000 ALTER TABLE `timetable_timetableslot` DISABLE KEYS */;
INSERT INTO `timetable_timetableslot` VALUES (1,'monday',1,'BAI702',2),(2,'monday',2,'BCS714C',2),(3,'monday',3,'',2),(4,'monday',4,'BAI701',2),(5,'monday',5,'BAD703',2),(6,'monday',6,'',2),(7,'monday',7,'',2),(8,'monday',8,'',2),(9,'tuesday',1,'BAI755X',2),(10,'tuesday',2,'BAD703',2),(11,'tuesday',3,'BAI702',2),(12,'tuesday',4,'BCS714C',2),(13,'tuesday',5,'BAI701',2),(14,'tuesday',6,'',2),(15,'tuesday',7,'',2),(16,'tuesday',8,'',2),(17,'wednesday',1,'BAI701',2),(18,'wednesday',2,'BAI702',2),(19,'wednesday',3,'BAI702(LAB)',2),(20,'wednesday',4,'BAI702(LAB)',2),(21,'wednesday',5,'BAD703',2),(22,'wednesday',6,'',2),(23,'wednesday',7,'',2),(24,'wednesday',8,'',2),(25,'thursday',1,'',2),(26,'thursday',2,'',2),(27,'thursday',3,'',2),(28,'thursday',4,'',2),(29,'thursday',5,'',2),(30,'thursday',6,'',2),(31,'thursday',7,'',2),(32,'thursday',8,'',2),(33,'friday',1,'',2),(34,'friday',2,'',2),(35,'friday',3,'',2),(36,'friday',4,'',2),(37,'friday',5,'',2),(38,'friday',6,'',2),(39,'friday',7,'',2),(40,'friday',8,'',2),(41,'saturday',1,'',2),(42,'saturday',2,'',2),(43,'saturday',3,'',2),(44,'saturday',4,'',2),(45,'saturday',5,'',2),(46,'saturday',6,'',2),(47,'saturday',7,'',2),(48,'saturday',8,'',2);
/*!40000 ALTER TABLE `timetable_timetableslot` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-07 19:06:57
