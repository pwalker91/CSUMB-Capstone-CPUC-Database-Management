# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.31-cll)
# Database: dyck5795
# Generation Time: 2015-02-13 21:45:58 +0000
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
  `OSName_OSArchitecture_OSVersion` varchar(30) DEFAULT NULL,
  `JavaVersion_JavaVendor` varchar(30) DEFAULT NULL,
  `DeviceID` varchar(30) DEFAULT NULL,
  `DeviceType` varchar(10) DEFAULT NULL,
  `Server` varchar(30) DEFAULT NULL,
  `Host` varchar(15) DEFAULT NULL,
  `NetworkCarrier` varchar(20) DEFAULT NULL,
  `NetworkProvider` varchar(30) DEFAULT NULL,
  `NewtworkOperator` varchar(30) DEFAULT NULL,
  `ConnectionType` varchar(30) DEFAULT NULL,
  `LocationID` int(7) DEFAULT NULL,
  `Tester` varchar(10) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL,
  `Latitude` double DEFAULT NULL,
  `Longitude` double DEFAULT NULL,
  `AvgLatitude` float DEFAULT NULL,
  `AvgLongitude` float DEFAULT NULL,
  `FileLocation` varchar(50) DEFAULT NULL,
  `Flag` tinyint(1) DEFAULT NULL,
  `FlagMessage` blob,
  `Timestamp` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Overview` WRITE;
/*!40000 ALTER TABLE `Overview` DISABLE KEYS */;

INSERT INTO `Overview` (`id`, `OSName_OSArchitecture_OSVersion`, `JavaVersion_JavaVendor`, `DeviceID`, `DeviceType`, `Server`, `Host`, `NetworkCarrier`, `NetworkProvider`, `NewtworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `AvgLatitude`, `AvgLongitude`, `FileLocation`, `Flag`, `FlagMessage`, `Timestamp`, `ErrorType`)
VALUES
	(1,'Linux;armv71;3.4.0-529760','0;The Android Project','99000344556962','mobile','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','1xrtt',2358,NULL,'2013-11-04','2013-11-04 14:48:23',40.70270919799805,-122.21016693115234,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

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
  `RTTMac` float DEFAULT NULL,
  `RTTAvg` float DEFAULT NULL,
  `MOS` float DEFAULT NULL,
  `RVal` float DEFAULT NULL,
  `ErrorType` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `PINGResult` WRITE;
/*!40000 ALTER TABLE `PINGResult` DISABLE KEYS */;

INSERT INTO `PINGResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `PacketsSent`, `PacketsReceived`, `PacketsLost`, `RTTMin`, `RTTMac`, `RTTAvg`, `MOS`, `RVal`, `ErrorType`)
VALUES
	(1,1,'west',1,4,4,0,481.293,622.223,526.405,1,86.0962,NULL),
	(2,1,'east',1,10,10,0,458.709,602.875,521.285,3.9,52.3598,NULL),
	(3,1,'west',2,10,10,0,483.765,628.632,551.474,2.3,52.3598,NULL);

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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `TCPResult` WRITE;
/*!40000 ALTER TABLE `TCPResult` DISABLE KEYS */;

INSERT INTO `TCPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `Port`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPeriod`, `UpPct`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPeriod`, `DownPct`, `ErrorType`)
VALUES
	(1,1,'west',1,'64',5003,528,532.784,557,10.25,0.7,1799,654.995,1978.5,12.3,1,NULL),
	(2,1,'east',1,'64',5003,21463,717.977,9011,10.025,1,21463,327.673,19274,10.525,1,NULL),
	(3,1,'west',2,'64',5003,168.4,332.653,1114,14.1,0.675,91.7,303.45,127.5,15.875,0.973254,NULL),
	(4,1,'east',2,'64',5003,19431,414.138,9141.5,10.3,1,25181,507.402,1187.5,10.1,0.89123,NULL);

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
  `WindowSize` float DEFAULT NULL,
  `ClientConnectedTo` varchar(15) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `DatagramLength` float DEFAULT NULL,
  `Jitter` float DEFAULT NULL,
  `Loss` float DEFAULT NULL,
  `Time` int(10) DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `UDPResult` WRITE;
/*!40000 ALTER TABLE `UDPResult` DISABLE KEYS */;

INSERT INTO `UDPResult` (`id`, `oid`, `ConnectionLoc`, `TestNumber`, `WindowSize`, `ClientConnectedTo`, `Port`, `DatagramLength`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(1,1,'west',1,220,'184.72.63.139',5004,160,9.374,0,5,NULL),
	(2,1,'west',1,220,'184.72.63.139',5004,160,12.645,0,5,NULL),
	(3,1,'west',1,220,'184.72.63.139',5004,160,8.214,0,5,NULL),
	(4,1,'east',1,220,'184.72.222.65',5004,160,23.301,0,5,NULL),
	(5,1,'east',1,220,'184.72.222.65',5004,160,12.952,1.234,1,NULL),
	(6,1,'east',1,220,'184.72.222.65',5004,160,12.844,0,1,NULL),
	(7,1,'west',2,220,'184.72.63.139',5004,160,12.633,0,1,NULL),
	(8,1,'east',2,220,'184.82.222.65',5004,160,12.252,1.234,1,NULL);

/*!40000 ALTER TABLE `UDPResult` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
