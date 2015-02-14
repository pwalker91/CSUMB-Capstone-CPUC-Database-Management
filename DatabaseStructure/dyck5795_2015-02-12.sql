# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.31-cll)
# Database: dyck5795
# Generation Time: 2015-02-13 00:25:37 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Device and Test Info
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Device and Test Info`;

CREATE TABLE `Device and Test Info` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `OSNAME;ARCHECTICUTRE;VERSION` varchar(30) DEFAULT NULL,
  `JAVAVERSION;VENDOR` varchar(30) DEFAULT NULL,
  `DeviceID` varchar(30) DEFAULT NULL,
  `DeviceType` varchar(10) DEFAULT NULL,
  `ServerName` varchar(30) DEFAULT NULL,
  `HostIpAddress` varchar(15) DEFAULT NULL,
  `NetworkCarrier` varchar(20) DEFAULT NULL,
  `NetworkProvider` varchar(30) DEFAULT NULL,
  `NewtworkOperator` varchar(30) DEFAULT NULL,
  `ConnectionType` varchar(30) DEFAULT NULL,
  `LocationID` int(7) DEFAULT NULL,
  `Tester` varchar(10) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` timestamp NULL DEFAULT NULL,
  `Latitude` float DEFAULT NULL,
  `Longitude` float DEFAULT NULL,
  `NormalLatitude` float DEFAULT NULL,
  `NormalLongitude` float DEFAULT NULL,
  `FileLocation` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Device and Test Info` WRITE;
/*!40000 ALTER TABLE `Device and Test Info` DISABLE KEYS */;

INSERT INTO `Device and Test Info` (`ID`, `OSNAME;ARCHECTICUTRE;VERSION`, `JAVAVERSION;VENDOR`, `DeviceID`, `DeviceType`, `ServerName`, `HostIpAddress`, `NetworkCarrier`, `NetworkProvider`, `NewtworkOperator`, `ConnectionType`, `LocationID`, `Tester`, `Date`, `Time`, `Latitude`, `Longitude`, `NormalLatitude`, `NormalLongitude`, `FileLocation`)
VALUES
	(1,'Linux;armv71;3.4.0-529760','0;The Android Project','99000344556962','mobile','Amazon West Server','184.72.63.139','Sprint','Sprint','Sprint','1xrtt',2358,NULL,'2013-11-04','2013-11-04 14:48:23',40.7027,-122.21,NULL,NULL,NULL);

/*!40000 ALTER TABLE `Device and Test Info` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table Ping Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Ping Test Results`;

CREATE TABLE `Ping Test Results` (
  `PINGID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `EastWest` varchar(5) DEFAULT NULL,
  `TestNumber` int(2) DEFAULT NULL,
  `PingedIPAddress` varchar(15) DEFAULT NULL,
  `PingsSent` float DEFAULT NULL,
  `PingsRecieved` float DEFAULT NULL,
  `PingsLost` float DEFAULT NULL,
  `MinTrip` float DEFAULT NULL,
  `MaxTrip` float DEFAULT NULL,
  `AvgTrip` float DEFAULT NULL,
  `MOS` float DEFAULT NULL,
  `RVal` float DEFAULT NULL,
  `ErrorType` int(11) DEFAULT NULL,
  PRIMARY KEY (`PINGID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `Ping Test Results` WRITE;
/*!40000 ALTER TABLE `Ping Test Results` DISABLE KEYS */;

INSERT INTO `Ping Test Results` (`PINGID`, `DeviceAndTestInfoID`, `EastWest`, `TestNumber`, `PingedIPAddress`, `PingsSent`, `PingsRecieved`, `PingsLost`, `MinTrip`, `MaxTrip`, `AvgTrip`, `MOS`, `RVal`, `ErrorType`)
VALUES
	(1,1,'west',1,'184.72.63.139',4,4,0,481.293,622.223,526.405,1,86.0962,NULL),
	(2,1,'east',1,'184.72.222.65',10,10,0,458.709,602.875,521.285,3.9,52.3598,NULL),
	(3,1,'west',2,'184.72.63.139',10,10,0,483.765,628.632,551.474,2.3,52.3598,NULL);

/*!40000 ALTER TABLE `Ping Test Results` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table TCP Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `TCP Test Results`;

CREATE TABLE `TCP Test Results` (
  `TCPID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `WindowSize` varchar(10) DEFAULT NULL,
  `ClientConnectedTo` varchar(15) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `EastWest` varchar(15) DEFAULT NULL,
  `TestNumber` int(11) DEFAULT NULL,
  `UpSpeed` float DEFAULT NULL,
  `UpStdDev` float DEFAULT NULL,
  `UpMedian` float DEFAULT NULL,
  `UpPR` float DEFAULT NULL,
  `UpPCT` float DEFAULT NULL,
  `DownSpeed` float DEFAULT NULL,
  `DownStdDev` float DEFAULT NULL,
  `DownMedian` float DEFAULT NULL,
  `DownPR` float DEFAULT NULL,
  `DownPCT` float DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`TCPID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `TCP Test Results` WRITE;
/*!40000 ALTER TABLE `TCP Test Results` DISABLE KEYS */;

INSERT INTO `TCP Test Results` (`TCPID`, `DeviceAndTestInfoID`, `WindowSize`, `ClientConnectedTo`, `Port`, `EastWest`, `TestNumber`, `UpSpeed`, `UpStdDev`, `UpMedian`, `UpPR`, `UpPCT`, `DownSpeed`, `DownStdDev`, `DownMedian`, `DownPR`, `DownPCT`, `ErrorType`)
VALUES
	(1,1,'64','184.72.63.139',5003,'west',1,528,532.784,557,10.25,0.7,1799,654.995,1978.5,12.3,1,NULL),
	(2,1,'64','184.72.222.65',5003,'east',1,21463,717.977,9011,10.025,1,21463,327.673,19274,10.525,1,NULL),
	(3,1,'64','184.72.63.139',5003,'west',2,168.4,332.653,1114,14.1,0.675,91.7,303.45,127.5,15.875,0.973254,NULL),
	(4,1,'64','184.72.222.65',5003,'east',2,19431,414.138,9141.5,10.3,1,25181,507.402,1187.5,10.1,0.89123,NULL);

/*!40000 ALTER TABLE `TCP Test Results` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table UDP Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `UDP Test Results`;

CREATE TABLE `UDP Test Results` (
  `UDPID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `EastWest` varchar(15) DEFAULT NULL,
  `TestNumber` int(11) DEFAULT NULL,
  `PartNumber` int(11) DEFAULT NULL,
  `WindowSize` float DEFAULT NULL,
  `ClientConnectedTo` varchar(15) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `DatagramLength` float DEFAULT NULL,
  `Jitter` float DEFAULT NULL,
  `Loss` float DEFAULT NULL,
  `Time` int(10) DEFAULT NULL,
  `ErrorType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`UDPID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `UDP Test Results` WRITE;
/*!40000 ALTER TABLE `UDP Test Results` DISABLE KEYS */;

INSERT INTO `UDP Test Results` (`UDPID`, `DeviceAndTestInfoID`, `EastWest`, `TestNumber`, `PartNumber`, `WindowSize`, `ClientConnectedTo`, `Port`, `DatagramLength`, `Jitter`, `Loss`, `Time`, `ErrorType`)
VALUES
	(1,1,'west',1,1,220,'184.72.63.139',5004,160,9.374,0,5,NULL),
	(2,1,'west',1,2,220,'184.72.63.139',5004,160,12.645,0,5,NULL),
	(3,1,'west',1,3,220,'184.72.63.139',5004,160,8.214,0,5,NULL),
	(4,1,'east',1,1,220,'184.72.222.65',5004,160,23.301,0,5,NULL),
	(5,1,'east',1,2,220,'184.72.222.65',5004,160,12.952,1.234,1,NULL),
	(6,1,'east',1,3,220,'184.72.222.65',5004,160,12.844,0,1,NULL),
	(7,1,'west',2,1,220,'184.72.63.139',5004,160,12.633,0,1,NULL),
	(8,1,'east',2,1,220,'184.82.222.65',5004,160,12.252,1.234,1,NULL);

/*!40000 ALTER TABLE `UDP Test Results` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
