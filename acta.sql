-- MySQL dump 10.13  Distrib 5.6.31, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: epsdatamining
-- ------------------------------------------------------
-- Server version	5.6.31-0ubuntu0.15.10.1

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
-- Table structure for table `acta`
--

DROP TABLE IF EXISTS `acta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `acta` (
  `idacta` int(11) NOT NULL AUTO_INCREMENT,
  `id_alu` int(11) DEFAULT NULL,
  `pla` varchar(45) DEFAULT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `codi_ruct` int(11) DEFAULT NULL,
  `assig` int(11) DEFAULT NULL,
  `curs` int(11) DEFAULT NULL,
  `tipus` varchar(45) DEFAULT NULL,
  `credits` int(11) DEFAULT NULL,
  `num_matric` int(11) DEFAULT NULL,
  `any` int(11) DEFAULT NULL,
  `convocatoria` varchar(45) DEFAULT NULL,
  `presentat` varchar(45) DEFAULT NULL,
  `mhonor` varchar(45) DEFAULT NULL,
  `nota` decimal(10,2) DEFAULT NULL,
  `qualificacio` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idacta`)
) ENGINE=InnoDB AUTO_INCREMENT=279892 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-22 12:31:12
