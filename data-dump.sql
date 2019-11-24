-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: e-report
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `username` varchar(250) NOT NULL,
  `title` varchar(250) NOT NULL,
  `subject` varchar(250) NOT NULL,
  `body` longtext NOT NULL,
  `admin` varchar(250) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `created_at_UNIQUE` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,1,'captain','Weekly report','Rejected report','The report you sent to me as your monthly report was not good enough you need to do  more please','Hr','2019-11-14 22:00:35'),(2,4,'diana','diana is testing employee\'s page','Good Job ! The  report is great','I like the work you submitted you did a terrific job','random','2019-11-22 18:13:23'),(3,3,'emeka','testing the employee task','You did a Good Job','<p>Hi I Just want to congratulate you for&nbsp; a job well done</p>','random','2019-11-23 12:32:25'),(4,4,'diana','diana is testing employee\'s page','Testing admin dashboard redirect','<p>I dont know if its working correctly</p>','diana','2019-11-23 15:58:12');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` varchar(250) NOT NULL,
  `file` varchar(250) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,'diana is testing employee\'s page','<p>Diana is testing employee&#39;s page.</p><p>Started here.</p><p>And ends here.</p>','codepictda.png',4,'2019-11-16 10:42:35','2019-11-17 05:01:13'),(2,'diana is testing employee\'s page','<p>Diana is testing employee&#39;s page.</p><p>Started here.</p><p>And ends here.</p>','codepictda.png',4,'2019-11-16 10:47:15',NULL),(3,'testing the employee task','<p>Yes! Emeka is testing this page</p>','codeplagovt.png',3,'2019-11-16 10:59:34','2019-11-16 17:04:42'),(7,'2nd report','<p>jasjssafkjsabfkjsaf</p><p>SAJSDBFJSBAFJKBHS</p>','',3,'2019-11-16 18:53:13','2019-11-17 06:00:55'),(8,'New post to do final testing','<p>Why are the files not been uploaded to a seperate file upload</p>','Screenshot from 2019-10-24 18-41-11.png',4,'2019-11-23 14:01:05',NULL);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(250) DEFAULT NULL,
  `email` varchar(250) DEFAULT NULL,
  `password` varchar(250) DEFAULT NULL,
  `is_admin` varchar(250) DEFAULT NULL,
  `firstname` varchar(250) DEFAULT NULL,
  `lastname` varchar(250) DEFAULT NULL,
  `image` longblob,
  `department` varchar(250) DEFAULT NULL,
  `position` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (3,'emeka','nnorukaemeka@gmail.com','$5$rounds=535000$xR8gF99ZHxnsMrtK$XtKFdIwfOQgaZPli5Rk1x0xzokSa3BuYuzJriMqyQ9.','0','Emeka','Nnoruka',_binary '39815753.jpeg','Backend','2'),(4,'diana','dianebassey@gmail.com','$5$rounds=535000$qmfGZShcrZYa1zaM$.5pYltACr0vomCTV/RgKk4mn4LwTkojE50C2//ELzp6','0','Diana','Bassey',_binary 'cpnews.png','Backend','3'),(5,'luchez','luchez@gmail.com','$5$rounds=535000$CuqAXQST6X1aDd02$wmzVl1mhWpLIL3lVfLEbU8YD0tA.ShQlnrm1.VZj666','1','Luchez','Nnoruka',_binary 'codeplagovt.png','Unijos','5');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-23 16:09:01
