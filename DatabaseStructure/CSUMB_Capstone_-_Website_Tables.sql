-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Fri Mar 20 05:47:54 UTC 2015




-- tables
-- Table HelpRequest
CREATE TABLE `HelpRequest` (
  `Id`              smallint(6)     NOT NULL AUTO_INCREMENT,
  `InsertTimestamp` timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Name`            varchar(80)     DEFAULT NULL,
  `Email`           varchar(80)     NOT NULL,
  `Subject`         varchar(30)     NOT NULL,
  `Message`         blob            NOT NULL,
  `PhoneNumber`     varchar(20)     DEFAULT NULL,
  `LastPageVisited` varchar(50)     NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table Query
CREATE TABLE `PageRequest` (
  `Id`                  int(11)     NOT NULL AUTO_INCREMENT,
  `InsertTimestamp`     timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `AnalysisOpts`        blob        NOT NULL,
  `ContactEmail`        varchar(80) NOT NULL,
  `ContactName`         varchar(80) DEFAULT NULL,
  `IsGenerated`         tinyint(1)  NOT NULL DEFAULT 0,
  `ErrorEncountered`    tinyint(1)  NOT NULL DEFAULT 0,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table Results
CREATE TABLE `PageResults` (
  `Id`              int(11)         NOT NULL AUTO_INCREMENT,
  `Fid`             int(11)         NOT NULL,
  `InsertTimestamp` timestamp       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CalculatedData`  blob            NOT NULL,
  `ImagePath`       varchar(300)    NOT NULL,
  `MetaInfo`        blob            NOT NULL,
  `PageHash`        varchar(10)     NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `Fid` (`Fid`),
  CONSTRAINT `pageresults_ibfk_1`
    FOREIGN KEY (`Fid`) REFERENCES `PageRequest` (`Id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- End of file.
