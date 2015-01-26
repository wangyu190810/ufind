-- MySQL dump 10.13  Distrib 5.6.19, for osx10.9 (x86_64)
--
-- Host: localhost    Database: ufind
-- ------------------------------------------------------
-- Server version	5.6.19

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
-- Table structure for table `blog`
--

DROP TABLE IF EXISTS `blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(80) DEFAULT NULL,
  `content_md` text,
  `tag` varchar(80) DEFAULT NULL,
  `classify` text,
  `content_html` text,
  `status` int(11) DEFAULT NULL,
  `img` varchar(80) DEFAULT NULL,
  `readNum` int(11) NOT NULL,
  `commentNum` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blog`
--

LOCK TABLES `blog` WRITE;
/*!40000 ALTER TABLE `blog` DISABLE KEYS */;
/*!40000 ALTER TABLE `blog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faculty` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `chiname` varchar(255) DEFAULT NULL,
  `university_id` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_faculty_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'APPP','哈哈哈','1'),(2,'BPPPP','黑黑','2'),(3,'APPP','文淡忘','1'),(4,'BPPPP','黑黑','1');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `major`
--

DROP TABLE IF EXISTS `major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `major` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `chiname` varchar(255) DEFAULT NULL,
  `university_id` varchar(225) DEFAULT NULL,
  `faculty_id` varchar(225) DEFAULT NULL,
  `introduction` varchar(2000) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `ix_major_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `major`
--

LOCK TABLES `major` WRITE;
/*!40000 ALTER TABLE `major` DISABLE KEYS */;
INSERT INTO `major` VALUES (1,NULL,NULL,'1','1','aaaaaa'),(2,NULL,NULL,'1','2','bbbbb'),(3,NULL,NULL,'1','4','12341234'),(4,'傻×',NULL,'1','1','aaaaaa'),(5,'wuwen',NULL,'1','2','bbbbb'),(6,'asdfasdf',NULL,'1','4','12341234');
/*!40000 ALTER TABLE `major` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `TOEFL_r` int(11) DEFAULT NULL,
  `TOEFL_l` int(11) DEFAULT NULL,
  `TOEFL_s` int(11) DEFAULT NULL,
  `TOEFL_w` int(11) DEFAULT NULL,
  `IELTS_r` int(11) DEFAULT NULL,
  `IELTS_l` int(11) DEFAULT NULL,
  `IELTS_s` int(11) DEFAULT NULL,
  `IELTS_w` int(11) DEFAULT NULL,
  `GRE_v` int(11) DEFAULT NULL,
  `GRE_q` int(11) DEFAULT NULL,
  `GRE_aw` int(11) DEFAULT NULL,
  `GMAT_v` int(11) DEFAULT NULL,
  `GMAT_q` int(11) DEFAULT NULL,
  `GMAT_aw` int(11) DEFAULT NULL,
  `GMAT_ir` int(11) DEFAULT NULL,
  `SAT_cr` int(11) DEFAULT NULL,
  `SAT_m` int(11) DEFAULT NULL,
  `STA_w` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),(2,123,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `university`
--

DROP TABLE IF EXISTS `university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `university` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `chiname` varchar(255) DEFAULT NULL,
  `schoollogo` varchar(255) DEFAULT NULL,
  `official` varchar(255) DEFAULT NULL,
  `baidu` varchar(255) DEFAULT NULL,
  `wiki` varchar(255) DEFAULT NULL,
  `menaGPA` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_university_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
INSERT INTO `university` VALUES (1,'MIT','麻省理工','http://7u2mbm.com1.z0.glb.clouddn.com/62037b5ajw1eodjjj1pckg20bo07au0x.gif',NULL,'http://baike.baidu.com/view/1935.htm',NULL,NULL,NULL,NULL,NULL,NULL),(2,'Stanford','斯坦福大学','qwerqwer',NULL,'http://baike.baidu.com/view/13725.htm',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `pic` varchar(255) DEFAULT NULL,
  `GPA` float DEFAULT NULL,
  `TOEFL` float DEFAULT NULL,
  `GRE` float DEFAULT NULL,
  `IELTS` float DEFAULT NULL,
  `GMAT` float DEFAULT NULL,
  `SAT` float DEFAULT NULL,
  `prevuniversity` varchar(225) DEFAULT NULL,
  `prevmajor` varchar(255) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'王玉','1234','123@qq.com',138044,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'东北电力',NULL,NULL,NULL),(2,'王er','1234','123@qq.com',1380441,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'xia',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-01-27  1:23:54
