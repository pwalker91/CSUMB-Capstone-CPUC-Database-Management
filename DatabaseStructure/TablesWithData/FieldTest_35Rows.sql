# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.17)
# Database: cpuc
# Generation Time: 2015-02-21 04:36:48 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Overview
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Overview`;

CREATE TABLE `Overview` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `OSName_OSArchitecture_OSVersion` varchar(30) DEFAULT NULL,
  `JavaVersion_JavaVendor` varchar(30) DEFAULT NULL,
  `DeviceID` varchar(30) DEFAULT NULL,
  `DeviceType` varchar(10) DEFAULT NULL,
  `Server` varchar(30) DEFAULT NULL,
  `Host` varchar(15) DEFAULT NULL,
  `NetworkCarrier` varchar(20) DEFAULT NULL,
  `NetworkProvider` varchar(30) DEFAULT NULL,
  `NetworkOperator` varchar(30) DEFAULT NULL,
  `ConnectionType` varchar(30) DEFAULT NULL,
  `LocationID` int(7) DEFAULT NULL,
  `Tester` varchar(10) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `AvgLatitude` float DEFAULT NULL,
  `AvgLongitude` float DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  `FileLocation` varchar(50) DEFAULT NULL,
  `Flag` tinyint(1) DEFAULT NULL,
  `FlagMessage` blob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf16;

LOCK TABLES `Overview` WRITE;
/*!40000 ALTER TABLE `Overview` DISABLE KEYS */;

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(1,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',1085,NULL,'2014-05-12','08:58:36',40.50657445,-122.3820429,40.5066,-122.382,'0',NULL,NULL,NULL),
	(2,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','EDGE',2064,NULL,'2014-05-13','07:51:07',0,0,0,0,'311',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(3,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',2054,NULL,'2014-05-13','12:54:35',0,0,0,0,'311',NULL,NULL,NULL),
	(4,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','EDGE',1683,NULL,'2014-05-14','10:57:45',0,0,0,0,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(5,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',2158,NULL,'2014-05-14','16:29:23',0,0,0,0,'311',NULL,NULL,NULL),
	(6,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-540242','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',2940,NULL,'2014-05-14','20:05:24',40.81507359,-121.98447055,40.8151,-121.984,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(7,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059514877','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',1550,NULL,'2014-04-29','15:57:34',0,0,0,0,'311',NULL,NULL,NULL),
	(8,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059704288','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',1200,NULL,'2013-11-04','09:32:49',34.17537582,-118.87669766,34.1754,-118.877,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(9,'2015-02-20 20:34:44','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059704288','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',1862,NULL,'2013-11-04','12:39:41',34.28311081,-119.23638445,34.2831,-119.236,'0',NULL,NULL,NULL),
	(10,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-2015522','0 | The Android Project','356420059704353','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',1254,NULL,'2014-05-12','15:09:38',37.34293404,-120.59995705,37.3429,-120.6,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(11,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-2015522','0 | The Android Project','356420059704353','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','EDGE',1407,NULL,'2014-05-13','15:08:01',35.41296648,-119.4905389,35.413,-119.491,'311',NULL,NULL,NULL),
	(12,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-2015522','0 | The Android Project','356420059704353','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','HSPA',1636,NULL,'2014-05-14','09:09:42',35.32896302,-120.83545801,35.329,-120.835,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(13,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-2015522','0 | The Android Project','356420059704353','Phone','Amazon West Server','184.72.63.139','AT&T','NA','AT&T','EDGE',2134,NULL,'2014-05-14','14:31:09',0,0,0,0,'311',NULL,NULL,NULL),
	(14,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-2015522','0 | The Android Project','356420059704353','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','HSPA',1729,NULL,'2014-05-15','12:46:56',36.94489525,-119.89635083,36.9449,-119.896,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(15,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059835355','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',2740,NULL,'2014-05-12','13:59:34',0,0,0,0,'311',NULL,NULL,NULL),
	(16,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059835355','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',2893,NULL,'2014-05-14','10:56:38',36.77906545,-119.89865495,36.7791,-119.899,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(17,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059835355','Phone','Amazon West Server','184.72.63.139','T-Mobile','NA','T-Mobile','LTE',2591,NULL,'2014-05-16','12:29:08',37.95330313,-121.29223196,37.9533,-121.292,'0',NULL,NULL,NULL),
	(18,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-529760','0 | The Android Project','99000344556962','Phone','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','1xRTT',2358,NULL,'2013-11-04','14:48:23',40.70170122,-122.21013722,40.7018,-122.21,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(19,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-529760','0 | The Android Project','99000344557036','Phone','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','EHRPD',1272,NULL,'2013-11-04','09:15:34',37.70374083,-121.92626831,37.7037,-121.926,'0',NULL,NULL,NULL),
	(20,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-529760','0 | The Android Project','99000344557519','Phone','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','LTE',1168,NULL,'2013-11-04','07:51:23',34.09930411,-118.32859584,34.0993,-118.329,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(21,'2015-02-20 20:34:45','Linux | armv7l | 3.4.0-529760','0 | The Android Project','99000344556964','Phone','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','LTE',2451,NULL,'2013-10-30','09:11:59',37.34601598,-121.96791609,37.346,-121.968,'0',NULL,NULL,NULL),
	(22,'2015-02-20 20:34:46','NA | NA | NA','NA | NA','WBBDTest8','Netbook','NA','NA','Verizon','Verizon','NA','NA',2141,NULL,'2013-10-30','08:01:19',33.106188,-116.131513,33.1062,-116.132,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(23,'2015-02-20 20:34:46','NA | NA | NA','NA | NA','NA','Netbook','NA','NA','NA','NA','NA','NA',1862,NULL,'2013-11-04','13:00:22',34.28302,-12.516971,34.283,-12.517,'0',NULL,NULL,NULL),
	(24,'2015-02-20 20:34:46','Linux | armv7l | 3.4.0-529760','0 | The Android Project','99000344556962','Phone','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','UNKNOWN',1972,NULL,'2013-11-05','08:56:14',39.92129875,-122.44720352,39.9213,-122.447,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(25,'2015-02-20 20:34:46','Linux | armv7l | 3.4.0-453951','0 | The Android Project','356420059463273','Phone','Amazon West Server','184.72.63.139','NA','NA','USA - Commnet','HSPAP',1115,NULL,'2013-10-24','11:24:15',36.45187525,-116.87007654,36.4519,-116.87,'0',NULL,NULL,NULL),
	(26,'2015-02-20 20:34:46','Linux | armv7l | 3.4.0-812098','0 | The Android Project','356567058425321','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',1006,NULL,'2013-10-22','10:53:37',33.65648119,-116.19718408,33.6565,-116.197,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(27,'2015-02-20 20:34:46','Linux | armv7l | 3.4.0-812098','0 | The Android Project','356567058250737','Phone','Amazon West Server','184.72.63.139','NA','NA','NA','UNKNOWN',1007,NULL,'2013-10-30','14:55:33',32.99890258,-116.84302156,32.9989,-116.843,'0',NULL,NULL,NULL),
	(28,'2015-02-20 20:34:46','NA | NA | NA','NA | NA','WBBDTest2','Netbook','NA','NA','T-Mobile','T-Mobile','NA','NA',2676,NULL,'2014-05-15','14:57:32',36.331438,-119.308815,36.3314,-119.309,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(29,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest2','Netbook','NA','NA','Verizon','Verizon','NA','NA',2591,NULL,'2014-05-16','12:29:04',37.95331,-121.292227,37.9533,-121.292,'0',NULL,NULL,NULL),
	(30,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest3','Netbook','NA','NA','AT&T','AT&T','NA','NA',2054,NULL,'2014-05-13','12:54:18',41.154882,-120.531922,41.1549,-120.532,'311',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(31,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest3','Netbook','NA','NA','AT&T','AT&T','NA','NA',2142,NULL,'2014-05-13','14:56:10',40.492805,-120.270773,40.4928,-120.27,'0',NULL,NULL,NULL),
	(32,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest3','Netbook','NA','NA','AT&T','AT&T','NA','NA',1110,NULL,'2014-05-14','08:39:12',40.438448,-120.635093,40.4384,-120.635,'0',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(33,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest3','Netbook','NA','NA','Sprint','Sprint','NA','NA',2135,NULL,'2014-05-14','12:04:38',40.517345,-121.015307,40.5173,-121.015,'311',NULL,NULL,NULL),
	(34,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest3','Netbook','NA','NA','Sprint','Sprint','NA','NA',1570,NULL,'2014-05-14','15:07:55',41.053017,-121.398758,41.053,-121.399,'311',NULL,NULL,NULL);

INSERT INTO `Overview` (`id`, `Timestamp`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NetworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `ErrorType`, `FileLocation`, `Flag`, `FlagMessage`)
VALUES
	(35,'2015-02-20 20:34:47','NA | NA | NA','NA | NA','WBBDTest4','Netbook','NA','NA','Verizon','Verizon','NA','NA',1311,NULL,'2013-11-04','08:42:09',37.811902,-121.996207,37.8119,-121.996,'0',NULL,NULL,NULL);

/*!40000 ALTER TABLE `Overview` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table PINGResult
# ------------------------------------------------------------

DROP TABLE IF EXISTS `PINGResult`;

CREATE TABLE `PINGResult` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `oid` int(10) DEFAULT NULL,
  `ConnectionLoc` varchar(5) DEFAULT NULL,
  `TestNumber` int(2) DEFAULT NULL,
  `PacketsSent` float DEFAULT NULL,
  `PacketsReceived` float DEFAULT NULL,
  `PacketsLost` float DEFAULT NULL,
  `RTTMin` float DEFAULT NULL,
  `RTTMax` float DEFAULT NULL,
  `RTTAverage` float DEFAULT NULL,
  `RValue` float DEFAULT NULL,
  `MOS` float DEFAULT NULL,
  `ErrorType` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `oid` (`oid`),
  CONSTRAINT `pingresult_ibfk_1` FOREIGN KEY (`oid`) REFERENCES `Overview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf16;

LOCK TABLES `PINGResult` WRITE;
/*!40000 ALTER TABLE `PINGResult` DISABLE KEYS */;

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(1,1,'East',3,10,10,0,132.752,246.827,189.856,74.8922,3.8,0),
	(2,1,'West',6,10,10,0,40.588,103.668,83.785,86.1924,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(3,4,'East',3,10,10,0,373.596,1269.93,778.994,-4.78442,1,0),
	(4,4,'West',6,10,10,0,272.309,7131.83,3152.65,-322.86,1,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(5,6,'East',3,10,10,0,238.434,516.601,357.94,51.6162,2.7,0),
	(6,6,'West',6,10,10,0,263.641,1384.34,603.964,18.679,1.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(7,8,'East',3,10,10,0,108.704,232.36,160.958,78.4625,4,0),
	(8,8,'West',6,10,10,0,61.219,105.346,94.238,85.9438,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(9,9,'East',3,10,10,0,102.692,495.331,194.064,75.8594,3.9,0),
	(10,9,'West',6,10,10,0,94.635,136.292,104.867,85.6901,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(11,10,'East',3,10,9,1,126.832,174.774,159.254,78.2403,4,0),
	(12,10,'West',6,10,10,0,81.695,1088.81,375.528,50.0406,2.6,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(13,12,'East',3,10,10,0,129.913,219.422,169.04,77.4869,3.9,0),
	(14,12,'West',6,10,10,0,70.495,135.04,111.566,85.5286,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(15,14,'East',3,10,9,1,350.464,572.388,451.49,39.0872,2,0),
	(16,14,'West',6,10,10,0,313.935,1074.34,446.572,39.7572,2.1,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(17,16,'East',3,10,10,0,120.727,238.22,173.608,76.6144,3.9,0),
	(18,16,'West',6,10,10,0,64.178,142.791,103.115,85.7328,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(19,17,'East',3,10,10,0,114.746,214.203,163.183,77.6285,3.9,0),
	(20,17,'West',6,10,10,0,41.504,100.83,81.008,86.2589,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(21,18,'East',3,10,10,0,458.709,602.875,521.285,29.7474,1.6,0),
	(22,18,'West',6,10,10,0,483.765,628.632,551.474,25.7006,1.4,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(23,19,'East',3,10,10,0,127.533,339.752,176.764,79.6855,4,0),
	(24,19,'West',6,10,10,0,51.055,114.471,84.036,86.1869,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(25,20,'East',3,10,10,0,97.198,145.446,111.196,85.5454,4.2,0),
	(26,20,'West',6,10,10,0,38.757,84.869,48.638,87.0341,4.3,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(27,21,'East',3,10,10,0,150.909,382.782,214.401,70.8586,3.6,0),
	(28,21,'West',6,10,10,0,44.068,132.05,90.997,86.0189,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(29,22,'East',3,10,10,0,111,431,214,72.3469,3.7,0),
	(30,22,'West',6,10,10,0,60,401,161,82.5593,4.1,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(31,23,'East',3,10,10,0,149,905,331,55.7972,2.9,0),
	(32,23,'West',6,10,8,2,58,1969,556,27.2609,1.5,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(33,24,'East',3,10,10,0,436.554,2337.86,988.015,-32.7904,1,0),
	(34,24,'West',6,10,10,0,486.359,813.72,565.011,23.8782,1.4,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(35,25,'East',3,10,10,0,226.014,546.356,271.628,63.167,3.3,0),
	(36,25,'West',6,10,10,0,178.101,4682.89,1619.71,-117.452,1,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(37,26,'East',3,10,10,0,150.94,253.021,187.497,74.4632,3.8,0),
	(38,26,'West',6,10,10,0,84.259,124.146,103.735,85.7172,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(39,27,'East',3,10,10,0,151.764,206.604,168.09,76.0006,3.9,0),
	(40,27,'West',6,10,10,0,81.482,125.244,95.425,85.914,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(41,28,'East',3,10,10,0,121,577,251,67.2951,3.5,0),
	(42,28,'West',6,10,10,0,60,418,201,76.4833,3.9,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(43,29,'East',3,10,10,0,108,213,166,78.3161,4,0),
	(44,29,'West',6,10,10,0,37,295,136,82.305,4.1,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(45,31,'East',3,10,10,0,144,191,160,76.9288,3.9,0),
	(46,31,'West',6,10,10,0,75,112,85,86.16,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(47,32,'East',3,10,10,0,154,197,173,75.859,3.9,0),
	(48,32,'West',6,10,10,0,76,129,101,85.7544,4.2,0);

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMax`, `RTTAverage`, `RValue`, `MOS`, `ErrorType`)
VALUES
	(49,35,'East',3,10,10,0,101,282,192,75.2681,3.8,0),
	(50,35,'West',6,10,10,0,30,224,99,84.9113,4.2,0);

/*!40000 ALTER TABLE `PINGResult` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table TCPResult
# ------------------------------------------------------------

DROP TABLE IF EXISTS `TCPResult`;

CREATE TABLE `TCPResult` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `oid` int(10) DEFAULT NULL,
  `ConnectionLoc` varchar(15) DEFAULT NULL,
  `TestNumber` int(11) DEFAULT NULL,
  `WindowSize` varchar(10) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `UpSpeed` float DEFAULT NULL,
  `UpStdDev` float DEFAULT NULL,
  `UpMedian` float DEFAULT NULL,
  `UpPeriod` float DEFAULT NULL,
  `UpPct` float DEFAULT NULL,
  `DownSpeed` float DEFAULT NULL,
  `DownStdDev` float DEFAULT NULL,
  `DownMedian` float DEFAULT NULL,
  `DownPeriod` float DEFAULT NULL,
  `DownPct` float DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `oid` (`oid`),
  CONSTRAINT `tcpresult_ibfk_1` FOREIGN KEY (`oid`) REFERENCES `Overview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf16;

LOCK TABLES `TCPResult` WRITE;
/*!40000 ALTER TABLE `TCPResult` DISABLE KEYS */;

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(1,1,'West',1,'32k',5005,4204,633.41,4162,10.025,1,13976,4030.01,14034,10.375,1,'0'),
	(2,1,'East',2,'32k',5005,3725,596.242,3834.5,10.05,1,14703,5764.95,16951,10.725,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(3,1,'West',4,'32k',5005,3850,569.469,3867.5,10.1,1,16715,2552.88,17027.5,10.225,1,'0'),
	(4,1,'East',5,'32k',5005,4514,1025,4686,10.125,1,13131,5863.6,14442,11.125,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(5,4,'West',1,'32k',5005,131.5,362.618,0,11.975,0.0869565,44.1,56.0131,0,17.725,0.275362,'0'),
	(6,4,'East',2,'32k',5005,110.5,279.258,0,17.075,0.0895522,54.9,57.6917,33.3,19.725,0.363636,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(7,4,'West',4,'32k',5005,0,0,0,0,0,0,0,0,0,0,'101'),
	(8,4,'East',5,'32k',5005,0,0,0,0,0,0,0,0,0,0,'101');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(9,6,'West',1,'32k',5005,125.1,267.677,0,14.825,0.0862069,69.8,36.8005,48.5,35.6,0.378571,'0'),
	(10,6,'East',2,'32k',5005,102.3,279.4,0,17,0.0757576,54.2,36.8725,43.2,32.2,0.519685,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(11,6,'West',4,'32k',5005,136.2,319.682,0,14.225,0.111111,45.9,44.4964,32.4,33.825,0.343284,'0'),
	(12,6,'East',5,'32k',5005,59.1,199.511,0,37.275,0.0544218,84,32.4111,59.35,44,0.402299,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(13,8,'West',1,'32k',5005,6154,1713.25,5866,10.3,0.975,15714,1990.95,15293,10.575,0.97561,'0'),
	(14,8,'East',2,'32k',5005,3979,2475.29,5603,10.1,0.8,12378,2963.55,13906.5,10.55,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(15,8,'West',4,'32k',5005,5671,285.676,5570.5,10.025,1,15789,1115.55,16280,10.55,1,'0'),
	(16,8,'East',5,'32k',5005,5225,291.266,5275,10.1,1,12598,2747.23,13016.5,10.475,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(17,9,'West',1,'32k',5005,13479,4137.92,15041,10.025,1,22066,5988.4,25179,10.35,1,'0'),
	(18,9,'East',2,'32k',5005,7629,606.503,7635.5,10.1,1,14899,9151.09,14755,10.6,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(19,9,'West',4,'32k',5005,380.5,1689.33,0,23,0.0449438,29100,6324.46,25293,11.3,0.909091,'0'),
	(20,9,'East',5,'32k',5005,8051,309.161,8028.5,10,1,20402,6813.29,21657,10.275,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(21,10,'West',1,'32k',5005,0,0,0,0,0,0,0,0,0,0,'102'),
	(22,10,'East',2,'32k',5005,1012,439.872,1081.5,10.425,0.8,12889,4479.47,14522,11.1,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(23,10,'West',4,'32k',5005,923,478.532,1048,10.825,0.902439,11979,4471.75,13346,11.4,0.909091,'0'),
	(24,10,'East',5,'32k',5005,909,413.308,787,10.525,0.829268,7536,3167.04,8216,11.375,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(25,12,'West',1,'32k',5005,8779,2160.26,7996,10.1,1,18631,3856.36,19145.5,10.5,1,'0'),
	(26,12,'East',2,'32k',5005,7010,860.758,7176.5,10.075,1,14306,4295.86,16237.5,10.425,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(27,12,'West',4,'32k',5005,11504,967.22,11305.5,10.025,1,13133,1560.64,13512,10.275,1,'0'),
	(28,12,'East',5,'32k',5005,7416,1026.45,7996,10,1,9992,3739.62,10370,10.325,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(29,14,'West',1,'32k',5005,49.9,215.608,0,32.025,0.031746,0,0,0,12.2,0,'0'),
	(30,14,'East',2,'32k',5005,0,0,0,0,0,0,0,0,0,0,'102');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(31,14,'West',4,'32k',5005,0,0,0,0,0,0,0,0,0,0,'101'),
	(32,14,'East',5,'32k',5005,0,0,0,0,0,0,0,0,0,0,'121');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(33,16,'West',1,'32k',5005,6233,267.513,6291.5,10.025,1,10506,1589.21,10803.5,10.425,1,'0'),
	(34,16,'East',2,'32k',5005,6305,434.194,6355.5,10.05,1,8268,1965.74,8615,10.375,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(35,16,'West',4,'32k',5005,6472,517.145,6488,10.05,1,6157,2380.79,5363,10.3,1,'0'),
	(36,16,'East',5,'32k',5005,6179,350.592,6258.5,10.05,1,4872,1940.59,5199,10.425,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(37,17,'West',1,'32k',5005,13751,1363.64,13500.5,10,1,23016,5480.64,23300.5,10.35,1,'0'),
	(38,17,'East',2,'32k',5005,7578,557.454,7340.5,10.1,1,17076,10746.3,13725.5,10.725,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(39,17,'West',4,'32k',5005,10673,1039.84,10682.5,10.05,1,22958,9101.06,24475.5,10.3,1,'0'),
	(40,17,'East',5,'32k',5005,7379,643.941,7471.5,10.1,1,10283,5444.29,11709,10.375,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(41,18,'West',1,'32k',5003,192.1,350.086,0,12.75,0.208333,76.7,40.5401,59.15,33.95,0.338346,'0'),
	(42,18,'East',2,'32k',5003,179,343.14,0,11.725,0.177778,101.6,48.5781,109.6,21.75,0.4,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(43,18,'West',4,'32k',5003,193.1,338.248,0,13.05,0.22,112.4,65.4061,120,30.325,0.386555,'0'),
	(44,18,'East',5,'32k',5003,186.7,309.328,65.5,13.55,0.207547,125.9,48.0921,131.6,24.85,0.408163,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(45,19,'West',1,'32k',5003,800,349.766,852,10.575,0.9,1733,486.186,1747.7,11.825,0.977273,'0'),
	(46,19,'East',2,'32k',5003,957,170.312,918,10.425,1,1236,649.792,869.5,11.9,0.978261,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(47,19,'West',4,'32k',5003,1024,221.32,983.5,10.15,1,1781,490.559,1708,11.325,1,'0'),
	(48,19,'East',5,'32k',5003,984,166.021,983,10.475,1,1238,402.094,1263.5,12.4,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(49,20,'West',1,'32k',5003,5870,530.653,5865.5,10.025,1,16768,6458.15,18151,10.65,0.97561,'0'),
	(50,20,'East',2,'32k',5003,6114,571.539,6323.5,10.1,1,10253,4001.43,9332,11.6,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(51,20,'West',4,'32k',5003,6441,663.819,6455,10.075,1,18862,4549.17,19821.5,10.8,1,'0'),
	(52,20,'East',5,'32k',5003,5297,742.059,5243,10.1,1,15491,6167.94,12510,10.95,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(53,21,'West',1,'32k',5003,3163,369.75,3113,10.3,1,7796,1420.2,7659,10.6,1,'0'),
	(54,21,'East',2,'32k',5003,3192,242.511,3112,10.075,1,7881,2310.92,8446,10.55,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(55,21,'West',4,'32k',5003,2475,308.516,2621,10.2,1,5234,1851.47,4826,11.75,0.954545,'0'),
	(56,21,'East',5,'32k',5003,2345,216.862,2293.5,10.15,1,6747,1465.94,7416,11.25,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(57,22,'West',1,'64k',5007,6538,388.535,6618.5,10.075,1,11810,1800.74,12162.5,10.5,1,'0'),
	(58,22,'East',2,'64k',5007,5852,1503.87,5537.5,10,1,10934,2719.82,11759,10.35,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(59,22,'West',4,'64k',5007,7144,409.446,7143.5,10.075,1,12040,959.897,12323.5,10.475,1,'0'),
	(60,22,'East',5,'64k',5007,7242,620.749,7437.5,10.075,1,10761,2660.3,11573,10.4,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(61,23,'West',1,'64k',5001,1283,665.898,1082,10.2,0.923077,7801,2634.27,8279,11.175,0.97619,'0'),
	(62,23,'East',2,'64k',5001,1057,683.352,851.75,10.525,0.923077,2977,1892.83,2762,12.25,0.895833,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(63,23,'West',4,'64k',5001,808,630.136,721.25,11.45,0.72093,12037,2568.61,11723,11.45,0.909091,'0'),
	(64,23,'East',5,'64k',5001,678,776.108,754.5,14.725,0.611111,6791,2692.48,7790,11.475,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(65,24,'West',1,'32k',5003,108.8,262.172,0,15.8,0.0655738,92.2,53.6066,98.6,35.925,0.321678,'0'),
	(66,24,'East',2,'32k',5003,184.6,323.034,0,11.95,0.170213,106.7,57.5159,120.5,29.35,0.391304,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(67,24,'West',4,'32k',5003,147.6,290.029,0,16.075,0.142857,112.7,55.1635,120.5,26.275,0.300971,'0'),
	(68,24,'East',5,'32k',5003,153.8,305.989,0,14.275,0.145455,122,51.7641,131.5,25.65,0.386139,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(69,25,'West',1,'32k',5005,137.9,273.351,0,13.325,0.0961538,37.7,46.9674,0,16.3,0.209677,'0'),
	(70,25,'East',2,'32k',5005,149.1,348.44,0,11.7,0.108696,42.9,42.2462,33.1,21.425,0.440476,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(71,25,'West',4,'32k',5005,0,0,0,0,0,0,0,0,0,0,'101'),
	(72,25,'East',5,'32k',5005,0,0,0,0,0,0,0,0,0,0,'101');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(73,26,'West',1,'32k',5001,987,461.405,918,10.65,0.902439,3341,1353.38,3191.65,12.125,0.893617,'0'),
	(74,26,'East',2,'32k',5001,1108,310.931,1016.5,10.325,1,5057,1838.61,5112,11.075,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(75,26,'West',4,'32k',5001,1004,380.444,918,10.375,1,4427,1641.35,5411,11.175,0.977273,'0'),
	(76,26,'East',5,'32k',5001,1079,286.342,1016,10.25,1,3244,1183.23,3623,11.6,0.977273,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(77,27,'West',1,'32k',5001,1199,314.959,1049,10.225,1,11698,3354.39,12696,10.85,1,'0'),
	(78,27,'East',2,'32k',5001,1195,290.575,1179.5,10.425,1,10323,3984.17,10976,10.65,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(79,27,'West',4,'32k',5001,1185,310.521,1082,10.4,1,12307,2860.98,12997,10.75,1,'0'),
	(80,27,'East',5,'32k',5001,1194,311.996,1114.5,10.375,1,10237,6034.96,43.1,13.975,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(81,28,'West',1,'64k',5005,1047.1,802.904,787,11.4,0.651163,5042,1190.54,4032,12.425,0.895833,'0'),
	(82,28,'East',2,'64k',5005,2112,1034.75,1933.75,10.275,0.894737,3581,1319.26,3618,11.225,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(83,28,'West',4,'64k',5005,1894,1100.85,1802.25,10.3,0.775,4262,1535.36,3987,11.675,0.977273,'0'),
	(84,28,'East',5,'64k',5005,2190,664.078,2163,10.2,0.975,3840,1386.51,4077,11.45,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(85,29,'West',1,'64k',5007,11329,1697.57,11141.5,10.05,1,25153,2334.95,25667.5,10.225,1,'0'),
	(86,29,'East',2,'64k',5007,9016,1577.43,9600.5,10.025,1,11301,3094.31,12354,10.35,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(87,29,'West',4,'64k',5007,8583,561.739,8225,10.05,1,22010,4466.56,20132,10.3,1,'0'),
	(88,29,'East',5,'64k',5007,9813,1430.06,9895.5,10.05,1,11967,3221.04,12754,10.35,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(89,31,'West',1,'64k',5001,1240,618.749,1113.75,10.45,0.925,3650,964.497,3961,11.525,1,'0'),
	(90,31,'East',2,'64k',5001,1209,565.396,1114.5,10.45,0.975,3307,1403.13,3584.5,12.2,0.93617,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(91,31,'West',4,'64k',5001,1269,660.99,1114,10.525,0.902439,3400,818.542,3579,11.575,1,'0'),
	(92,31,'East',5,'64k',5001,1262,666.411,1115,10.375,0.925,3480,1260.44,3906,11.775,0.954545,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(93,32,'West',1,'64k',5001,263.5,586.825,0,18.25,0.246377,2079,2445.63,0,19.5,0.4,'0'),
	(94,32,'East',2,'64k',5001,817.3,712.729,98.25,19.425,0.660377,1036,1329,0,23.55,0.467391,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(95,32,'West',4,'64k',5001,105.8,540.585,0,24.9,0.0645161,1718,1832.18,147.1,12.425,0.404255,'0'),
	(96,32,'East',5,'64k',5001,144.8,389.637,0,34.525,0.154472,2545,2471.88,1517.95,17.225,0.477612,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(97,35,'West',1,'64k',5007,12531,2256.86,12615.5,10.025,1,27338,5104.95,26749,10.525,0.97561,'0'),
	(98,35,'East',2,'64k',5007,11529,1281.21,11961,10.025,1,13282,3534.5,14163.5,10.35,1,'0');

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(99,35,'West',4,'64k',5007,12218,724.558,12125,10.05,1,25306,3081.2,25608.5,10.375,1,'0'),
	(100,35,'East',5,'64k',5007,10835,2850.36,11076.5,10,1,12816,2919.05,13884.5,10.325,1,'0');

/*!40000 ALTER TABLE `TCPResult` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table UDPResult
# ------------------------------------------------------------

DROP TABLE IF EXISTS `UDPResult`;

CREATE TABLE `UDPResult` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `oid` int(10) DEFAULT NULL,
  `ConnectionLoc` varchar(15) DEFAULT NULL,
  `TestNumber` int(11) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `DatagramSize` float DEFAULT NULL,
  `Jitter` float DEFAULT NULL,
  `Loss` float DEFAULT NULL,
  `Time` int(10) DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `oid` (`oid`),
  CONSTRAINT `udpresult_ibfk_1` FOREIGN KEY (`oid`) REFERENCES `Overview` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf16;

LOCK TABLES `UDPResult` WRITE;
/*!40000 ALTER TABLE `UDPResult` DISABLE KEYS */;

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(1,1,'West',7,5006,220,10.37,0,1,'0'),
	(2,1,'West',7,5006,220,7.689,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(3,1,'West',7,5006,220,9.521,0,1,'0'),
	(4,1,'East',8,5006,220,9.248,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(5,1,'East',8,5006,220,9.902,0,1,'0'),
	(6,1,'East',8,5006,220,12.806,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(7,1,'West',9,5006,220,7.796,0,5,'0'),
	(8,1,'East',10,5006,220,13.712,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(9,4,'West',7,5006,220,18.48,0,1,'0'),
	(10,4,'West',7,5006,220,26.79,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(11,4,'West',7,5006,220,23.151,0,1,'0'),
	(12,4,'East',8,5006,220,25.983,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(13,4,'East',8,5006,220,32.012,0,1,'0'),
	(14,4,'East',8,5006,220,46.176,3.92,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(15,4,'West',9,5006,220,32.829,0,5,'0'),
	(16,4,'East',10,5006,220,27.407,4.78,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(17,6,'West',7,5006,220,37.275,0,1,'0'),
	(18,6,'West',7,5006,220,19.943,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(19,6,'West',7,5006,220,4.75,0,1,'0'),
	(20,6,'East',8,5006,220,4.502,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(21,6,'East',8,5006,220,30.896,0,1,'0'),
	(22,6,'East',8,5006,220,20.489,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(23,6,'West',9,5006,220,58.473,0,5,'0'),
	(24,6,'East',10,5006,220,15.104,13.54,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(25,8,'West',7,5006,220,13.696,0,1,'0'),
	(26,8,'West',7,5006,220,11.708,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(27,8,'West',7,5006,220,11.497,0,1,'0'),
	(28,8,'East',8,5006,220,12.955,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(29,8,'East',8,5006,220,13.464,0,1,'0'),
	(30,8,'East',8,5006,220,11.981,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(31,8,'West',9,5006,220,14.935,0,5,'0'),
	(32,8,'East',10,5006,220,24.486,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(33,9,'West',7,5006,220,8.159,0,1,'0'),
	(34,9,'West',7,5006,220,12.493,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(35,9,'West',7,5006,220,7.018,0,1,'0'),
	(36,9,'East',8,5006,220,14.881,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(37,9,'East',8,5006,220,11.723,0,1,'0'),
	(38,9,'East',8,5006,220,19.138,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(39,9,'West',9,5006,220,9.057,0,5,'0'),
	(40,9,'East',10,5006,220,15.649,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(41,10,'West',7,5006,220,13.661,0,1,'0'),
	(42,10,'West',7,5006,220,6.036,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(43,10,'West',7,5006,220,12.164,0,1,'0'),
	(44,10,'East',8,5006,220,6.392,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(45,10,'East',8,5006,220,8.883,0,1,'0'),
	(46,10,'East',8,5006,220,4.856,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(47,10,'West',9,5006,220,10.436,0,5,'0'),
	(48,10,'East',10,5006,220,7.532,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(49,12,'West',7,5006,220,11.554,0,1,'0'),
	(50,12,'West',7,5006,220,11.71,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(51,12,'West',7,5006,220,10.86,0,1,'0'),
	(52,12,'East',8,5006,220,17.281,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(53,12,'East',8,5006,220,16.335,0,1,'0'),
	(54,12,'East',8,5006,220,14.462,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(55,12,'West',9,5006,220,3.861,0,5,'0'),
	(56,12,'East',10,5006,220,17.857,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(57,14,'West',7,5006,220,115.631,0,1,'0'),
	(58,14,'West',7,5006,220,84.085,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(59,14,'West',7,5006,220,96.921,0,1,'0'),
	(60,14,'East',8,5006,220,115.583,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(61,14,'East',8,5006,220,78.995,0,1,'0'),
	(62,14,'East',8,5006,220,100.562,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(63,14,'West',9,5006,220,0,0,5,'131'),
	(64,14,'East',10,5006,220,0,0,5,'131');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(65,16,'West',7,5006,220,10.621,0,1,'0'),
	(66,16,'West',7,5006,220,13.244,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(67,16,'West',7,5006,220,11.868,0,1,'0'),
	(68,16,'East',8,5006,220,10.642,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(69,16,'East',8,5006,220,10.857,0,1,'0'),
	(70,16,'East',8,5006,220,13.876,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(71,16,'West',9,5006,220,11.15,0,5,'0'),
	(72,16,'East',10,5006,220,12.483,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(73,17,'West',7,5006,220,8.862,0,1,'0'),
	(74,17,'West',7,5006,220,7.936,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(75,17,'West',7,5006,220,7.437,0,1,'0'),
	(76,17,'East',8,5006,220,10.845,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(77,17,'East',8,5006,220,10.629,0,1,'0'),
	(78,17,'East',8,5006,220,14.036,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(79,17,'West',9,5006,220,12.265,0,5,'0'),
	(80,17,'East',10,5006,220,12.256,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(81,18,'West',7,5004,220,27.827,0,1,'0'),
	(82,18,'West',7,5004,220,13.2,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(83,18,'West',7,5004,220,12.912,0,1,'0'),
	(84,18,'East',8,5004,220,18.522,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(85,18,'East',8,5004,220,20.873,0,1,'0'),
	(86,18,'East',8,5004,220,11.918,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(87,18,'West',9,5004,220,19.404,0,5,'0'),
	(88,18,'East',10,5004,220,42.777,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(89,19,'West',7,5004,220,18.403,0,1,'0'),
	(90,19,'West',7,5004,220,19.456,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(91,19,'West',7,5004,220,14.95,0,1,'0'),
	(92,19,'East',8,5004,220,15.589,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(93,19,'East',8,5004,220,12.66,0,1,'0'),
	(94,19,'East',8,5004,220,12.483,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(95,19,'West',9,5004,220,17.081,0.39,5,'0'),
	(96,19,'East',10,5004,220,15.929,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(97,20,'West',7,5004,220,1.197,0,1,'0'),
	(98,20,'West',7,5004,220,5.045,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(99,20,'West',7,5004,220,2.362,0,1,'0'),
	(100,20,'East',8,5004,220,5.628,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(101,20,'East',8,5004,220,6.442,0,1,'0'),
	(102,20,'East',8,5004,220,6.735,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(103,20,'West',9,5004,220,6.334,0,5,'0'),
	(104,20,'East',10,5004,220,0.919,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(105,21,'West',7,5004,220,12.857,0,1,'0'),
	(106,21,'West',7,5004,220,13.838,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(107,21,'West',7,5004,220,14.853,0,1,'0'),
	(108,21,'East',8,5004,220,22.175,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(109,21,'East',8,5004,220,18.339,1.96,1,'0'),
	(110,21,'East',8,5004,220,17.957,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(111,21,'West',9,5004,220,12.741,0,5,'0'),
	(112,21,'East',10,5004,220,20.495,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(113,22,'West',7,5008,220,8.467,0,1,'0'),
	(114,22,'West',7,5008,220,5.966,1.92,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(115,22,'West',7,5008,220,12.415,0,1,'0'),
	(116,22,'East',8,5008,220,10.719,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(117,22,'East',8,5008,220,12.454,1.96,1,'0'),
	(118,22,'East',8,5008,220,11.806,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(119,22,'West',9,5008,220,6.705,0,5,'0'),
	(120,22,'East',10,5008,220,10.959,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(121,23,'West',7,5002,220,24.416,0,1,'0'),
	(122,23,'West',7,5002,220,91.583,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(123,23,'West',7,5002,220,22.697,0,1,'0'),
	(124,23,'East',8,5002,220,21.321,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(125,23,'East',8,5002,220,20.574,0,1,'0'),
	(126,23,'East',8,5002,220,24.502,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(127,23,'West',9,5002,220,15.145,0,5,'0'),
	(128,23,'East',10,5002,220,16.67,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(129,24,'West',7,5004,220,24.81,0,1,'0'),
	(130,24,'West',7,5004,220,25.91,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(131,24,'West',7,5004,220,9.642,0,1,'0'),
	(132,24,'East',8,5004,220,22.556,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(133,24,'East',8,5004,220,17.914,0,1,'0'),
	(134,24,'East',8,5004,220,17.332,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(135,24,'West',9,5004,220,9.939,0,5,'0'),
	(136,24,'East',10,5004,220,13.161,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(137,25,'West',7,5006,220,13.674,0,1,'0'),
	(138,25,'West',7,5006,220,12.873,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(139,25,'West',7,5006,220,15.931,0,1,'0'),
	(140,25,'East',8,5006,220,16.332,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(141,25,'East',8,5006,220,14.098,0,1,'0'),
	(142,25,'East',8,5006,220,17.699,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(143,25,'West',9,5006,220,15.974,0,5,'0'),
	(144,25,'East',10,5006,220,16.597,0.79,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(145,26,'West',7,5002,220,11.722,0,1,'0'),
	(146,26,'West',7,5002,220,10.585,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(147,26,'West',7,5002,220,12.212,0,1,'0'),
	(148,26,'East',8,5002,220,16.693,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(149,26,'East',8,5002,220,15.881,0,1,'0'),
	(150,26,'East',8,5002,220,14.365,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(151,26,'West',9,5002,220,5.496,0,5,'0'),
	(152,26,'East',10,5002,220,14.609,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(153,27,'West',7,5002,220,10.152,0,1,'0'),
	(154,27,'West',7,5002,220,5.14,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(155,27,'West',7,5002,220,9.582,0,1,'0'),
	(156,27,'East',8,5002,220,13.717,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(157,27,'East',8,5002,220,16.147,0,1,'0'),
	(158,27,'East',8,5002,220,11.048,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(159,27,'West',9,5002,220,10.322,0,5,'0'),
	(160,27,'East',10,5002,220,11.97,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(161,28,'West',7,5006,220,6.787,0,1,'0'),
	(162,28,'West',7,5006,220,8.119,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(163,28,'West',7,5006,220,9.621,0,1,'0'),
	(164,28,'East',8,5006,220,14.922,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(165,28,'East',8,5006,220,9.97,0,1,'0'),
	(166,28,'East',8,5006,220,10.488,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(167,28,'West',9,5006,220,6.213,0,5,'0'),
	(168,28,'East',10,5006,220,19.973,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(169,29,'West',7,5008,220,11.124,1.96,1,'0'),
	(170,29,'West',7,5008,220,13.163,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(171,29,'West',7,5008,220,11.377,1.96,1,'0'),
	(172,29,'East',8,5008,220,12.73,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(173,29,'East',8,5008,220,15.022,1.96,1,'0'),
	(174,29,'East',8,5008,220,12.549,1.92,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(175,29,'West',9,5008,220,11.319,0,5,'0'),
	(176,29,'East',10,5008,220,18.998,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(177,31,'West',7,5002,220,14.216,0,1,'0'),
	(178,31,'West',7,5002,220,10.916,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(179,31,'West',7,5002,220,10.631,0,1,'0'),
	(180,31,'East',8,5002,220,12.438,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(181,31,'East',8,5002,220,14.437,0,1,'0'),
	(182,31,'East',8,5002,220,12.62,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(183,31,'West',9,5002,220,10.529,0.39,5,'0'),
	(184,31,'East',10,5002,220,13.248,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(185,32,'West',7,5002,220,10.263,0,1,'0'),
	(186,32,'West',7,5002,220,10.737,1.96,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(187,32,'West',7,5002,220,7.648,0,1,'0'),
	(188,32,'East',8,5002,220,14.544,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(189,32,'East',8,5002,220,15.614,0,1,'0'),
	(190,32,'East',8,5002,220,11.427,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(191,32,'West',9,5002,220,13.473,0,5,'0'),
	(192,32,'East',10,5002,220,14.827,0,5,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(193,35,'West',7,5008,220,11.488,0,1,'0'),
	(194,35,'West',7,5008,220,11.581,0,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(195,35,'West',7,5008,220,8.042,0,1,'0'),
	(196,35,'East',8,5008,220,10.083,4,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(197,35,'East',8,5008,220,12.575,0,1,'0'),
	(198,35,'East',8,5008,220,11.665,4,1,'0');

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `Port`, `DatagramSize`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(199,35,'West',9,5008,220,6.458,0,5,'0'),
	(200,35,'East',10,5008,220,13.157,0.39,5,'0');

/*!40000 ALTER TABLE `UDPResult` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
