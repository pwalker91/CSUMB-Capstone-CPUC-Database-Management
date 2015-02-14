# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.31-cll)
# Database: CPUCSQLDATABASE
# Generation Time: 2015-02-09 06:46:31 +0000
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
  `OSNAME;ARCHECTICUTRE;VERSION;JAVAVERSION;VENDORv` varchar(30) DEFAULT NULL,
  `Latitude` varchar(20) DEFAULT NULL,
  `Longitude` varchar(20) DEFAULT NULL,
  `Network Type` varchar(20) DEFAULT NULL,
  `Server Name` varchar(30) DEFAULT NULL,
  `Host Ip Address` varchar(15) DEFAULT NULL,
  `Network Provider` varchar(30) DEFAULT NULL,
  `Newtwork Operator` varchar(30) DEFAULT NULL,
  `Device ID` int(30) DEFAULT NULL,
  `Device Type` varchar(10) DEFAULT NULL,
  `Connection Type` varchar(30) DEFAULT NULL,
  `Location ID` int(7) DEFAULT NULL,
  `Tester` varchar(10) DEFAULT NULL,
  `Date` varchar(30) DEFAULT NULL,
  `Time` varchar(10) DEFAULT NULL,
  `Network` varchar(10) DEFAULT NULL,
  `Census 2010` varchar(10) DEFAULT NULL,
  `R5Coverage` varchar(10) DEFAULT NULL,
  `Normal Latitude` varchar(20) DEFAULT NULL,
  `Normal Longitude` varchar(20) DEFAULT NULL,
  `Data File Location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

LOCK TABLES `Device and Test Info` WRITE;
/*!40000 ALTER TABLE `Device and Test Info` DISABLE KEYS */;

INSERT INTO `Device and Test Info` (`ID`, `OSNAME;ARCHECTICUTRE;VERSION;JAVAVERSION;VENDORv`, `Latitude`, `Longitude`, `Network Type`, `Server Name`, `Host Ip Address`, `Network Provider`, `Newtwork Operator`, `Device ID`, `Device Type`, `Connection Type`, `Location ID`, `Tester`, `Date`, `Time`, `Network`, `Census 2010`, `R5Coverage`, `Normal Latitude`, `Normal Longitude`, `Data File Location`)
VALUES
	(2,NULL,'12..12341234','0.999999999999999999',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

/*!40000 ALTER TABLE `Device and Test Info` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table Ping Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Ping Test Results`;

CREATE TABLE `Ping Test Results` (
  `PINGID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `East West (Test Number)` varchar(15) DEFAULT NULL,
  `Pinged IP Address` varchar(15) DEFAULT NULL,
  `Pings Sent` varchar(10) DEFAULT NULL,
  `Pings Recieved` varchar(10) DEFAULT NULL,
  `Pings Lost` varchar(10) DEFAULT NULL,
  `MinTrip` varchar(10) DEFAULT NULL,
  `MaxTrip` varchar(10) DEFAULT NULL,
  `AvgTrip` varchar(10) DEFAULT NULL,
  `MOS` varchar(10) DEFAULT NULL,
  `RVal` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`PINGID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table TCP Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `TCP Test Results`;

CREATE TABLE `TCP Test Results` (
  `TCPID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `Window Size` varchar(10) DEFAULT NULL,
  `Client Connected To` varchar(15) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `Latitude` varchar(20) DEFAULT NULL,
  `Longitude` varchar(20) DEFAULT NULL,
  `East West (Test Number)` varchar(15) DEFAULT NULL,
  `Up Speed` varchar(25) DEFAULT NULL,
  `Down Speed` varchar(25) DEFAULT NULL,
  `Up Standard Deviation` varchar(25) DEFAULT NULL,
  `Down Standard Deviation` varchar(25) DEFAULT NULL,
  `Up Median` varchar(25) DEFAULT NULL,
  `Down Median` varchar(25) DEFAULT NULL,
  `Up PR` varchar(25) DEFAULT NULL,
  `Up PCT` varchar(25) DEFAULT NULL,
  `Down PR` varchar(25) DEFAULT NULL,
  `Down PCT` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`TCPID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table UDP Test Results
# ------------------------------------------------------------

DROP TABLE IF EXISTS `UDP Test Results`;

CREATE TABLE `UDP Test Results` (
  `UDPID` int(10) NOT NULL AUTO_INCREMENT,
  `DeviceAndTestInfoID` int(10) DEFAULT NULL,
  `Window Size` varchar(20) DEFAULT NULL,
  `Client Connected To` varchar(15) DEFAULT NULL,
  `Port` int(5) DEFAULT NULL,
  `Datagram Length` varchar(15) DEFAULT NULL,
  `Latitude` varchar(20) DEFAULT NULL,
  `Longitude` varchar(20) DEFAULT NULL,
  `Jitter` varchar(10) DEFAULT NULL,
  `Loss` varchar(10) DEFAULT NULL,
  `Time` varchar(10) DEFAULT NULL,
  `East West (Test Number)` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`UDPID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
