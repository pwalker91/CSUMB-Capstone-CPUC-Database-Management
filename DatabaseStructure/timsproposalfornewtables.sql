# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.31-cll)
# Database: dyck5795
# Generation Time: 2015-03-06 17:09:58 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Help
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Help`;

CREATE TABLE `Help` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `Name` varchar(25) NOT NULL DEFAULT '',
  `Email` varchar(25) NOT NULL DEFAULT '',
  `Subject` varchar(25) NOT NULL DEFAULT '',
  `Date` date NOT NULL,
  `Message` varchar(200) NOT NULL DEFAULT '',
  `Contact` varchar(25) DEFAULT '',
  `PhoneNumber` int(11) DEFAULT NULL,
  `LastPageVisited` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table Popular
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Popular`;

CREATE TABLE `Popular` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `Query` varchar(100) DEFAULT NULL,
  `DateFirst` date DEFAULT NULL,
  `DateLast` date DEFAULT NULL,
  `NumberOfQueries` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table Query
# ------------------------------------------------------------

DROP TABLE IF EXISTS `Query`;

CREATE TABLE `Query` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ImageLoc` longblob,
  `Query` varchar(100) DEFAULT NULL,
  `DateQueried` datetime DEFAULT NULL,
  `Hits` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
