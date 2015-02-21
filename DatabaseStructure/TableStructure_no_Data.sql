# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.6.17)
# Database: cpuc
# Generation Time: 2015-02-21 04:33:16 +0000
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




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
