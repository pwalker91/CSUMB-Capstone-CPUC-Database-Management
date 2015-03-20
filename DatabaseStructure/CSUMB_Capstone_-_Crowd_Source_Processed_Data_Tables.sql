-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Fri Mar 20 05:52:31 UTC 2015




-- tables
-- Table `FileInfo`
CREATE TABLE `FileInfo` (
    `Id` int    NOT NULL  AUTO_INCREMENT,
    `InsertTimestamp` timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ,
    `DeviceID` varchar(30)    NULL ,
    `DeviceType` varchar(10)    NOT NULL ,
    `AppVersion` varchar(10)    NOT NULL ,
    `NetworkCarrier` varchar(20)    NOT NULL ,
    `NetworkProvider` varchar(30)    NULL DEFAULT NULL ,
    `NetworkOperator` varchar(30)    NULL DEFAULT NULL ,
    `ConnectionType` varchar(30)    NULL DEFAULT NULL ,
    `ConnectionName` varchar(30)    NOT NULL ,
    `Roaming` bool    NOT NULL ,
    `Environment` varchar(20)    NULL DEFAULT NULL ,
    `Date` date    NOT NULL ,
    `Time` time    NOT NULL ,
    `PhoneModel` varchar(30)    NOT NULL ,
    `PhoneManufac` varchar(30)    NOT NULL ,
    `PhoneAPIVer` varchar(30)    NOT NULL ,
    `PhoneSDKVer` varchar(30)    NOT NULL ,
    `OSName` varchar(30)    NULL DEFAULT NULL ,
    `OSArchitecture` varchar(30)    NULL ,
    `OSVersion` varchar(10)    NULL ,
    `JavaVersion` varchar(10)    NULL DEFAULT NULL ,
    `JavaVendor` varchar(20)    NULL ,
    `Server` varchar(30)    NULL DEFAULT NULL ,
    `Host` varchar(15)    NULL DEFAULT NULL ,
    `LocationSource` varchar(10)    NOT NULL ,
    `Latitude` double(15,11)    NULL DEFAULT NULL ,
    `Longitude` double(15,11)    NULL DEFAULT NULL ,
    `DistanceMoved` double(10,5)    NOT NULL ,
    `ErrorType` int    NOT NULL DEFAULT 0 ,
    `FileLocation` varchar(50)    NULL DEFAULT NULL ,
    `Flag` bool    NOT NULL ,
    `FlagMessage` blob    NULL ,
    CONSTRAINT `Overview_pk` PRIMARY KEY (`Id`)
) ENGINE InnoDB
;

-- Table `PINGResults`
CREATE TABLE `PINGResults` (
    `Id` int    NOT NULL  AUTO_INCREMENT,
    `Oid` int    NOT NULL ,
    `ConnectionLoc` varchar(6)    NOT NULL ,
    `TestNumber` int    NULL DEFAULT NULL ,
    `PacketsSent` int    NULL DEFAULT NULL ,
    `PacketsReceived` int    NULL DEFAULT NULL ,
    `PacketsLost` int    NULL DEFAULT NULL ,
    `RTTMin` double(8,4)    NULL DEFAULT NULL ,
    `RTTMax` double(8,4)    NULL DEFAULT NULL ,
    `RTTAverage` double(8,4)    NULL DEFAULT NULL ,
    `RValue` double(8,4)    NULL DEFAULT NULL ,
    `MOS` double(2,1)    NULL DEFAULT NULL ,
    `ErrorType` varchar(30)    NULL DEFAULT NULL ,
    CONSTRAINT `PINGResult_pk` PRIMARY KEY (`Id`)
) ENGINE InnoDB
;

CREATE INDEX `oid` ON `PINGResults` (`Oid`);


-- Table `TCPResults`
CREATE TABLE `TCPResults` (
    `Id` int    NOT NULL  AUTO_INCREMENT,
    `Oid` int    NOT NULL ,
    `ConnectionLoc` varchar(6)    NOT NULL ,
    `TestNumber` int    NULL ,
    `WindowSize` varchar(10)    NULL DEFAULT NULL ,
    `Port` int    NULL DEFAULT NULL ,
    `UpSpeed` double(11,5)    NULL DEFAULT NULL ,
    `UpStdDev` double(11,5)    NULL DEFAULT NULL ,
    `UpMedian` double(11,5)    NULL DEFAULT NULL ,
    `UpPeriod` double(6,3)    NULL DEFAULT NULL ,
    `UpPct` double(8,6)    NULL DEFAULT NULL ,
    `DownSpeed` double(11,5)    NULL DEFAULT NULL ,
    `DownStdDev` double(11,5)    NULL DEFAULT NULL ,
    `DownMedian` double(11,5)    NULL DEFAULT NULL ,
    `DownPeriod` double(6,3)    NULL DEFAULT NULL ,
    `DownPct` double(8,6)    NULL DEFAULT NULL ,
    `ErrorType` varchar(30)    NULL ,
    CONSTRAINT `TCPResult_pk` PRIMARY KEY (`Id`)
) ENGINE InnoDB
;

CREATE INDEX `oid` ON `TCPResults` (`Oid`);


-- Table `UDPResults`
CREATE TABLE `UDPResults` (
    `Id` int    NOT NULL  AUTO_INCREMENT,
    `Oid` int    NOT NULL ,
    `ConnectionLoc` varchar(6)    NOT NULL ,
    `TestNumber` int    NULL DEFAULT NULL ,
    `Port` int    NULL DEFAULT NULL ,
    `DatagramSize` int    NULL DEFAULT NULL ,
    `Jitter` double(8,5)    NULL DEFAULT NULL ,
    `Loss` double(8,6)    NULL DEFAULT NULL ,
    `Time` int    NULL DEFAULT NULL ,
    `ErrorType` varchar(30)    NULL DEFAULT NULL ,
    CONSTRAINT `UDPResult_pk` PRIMARY KEY (`Id`)
) ENGINE InnoDB
;

CREATE INDEX `oid` ON `UDPResults` (`Oid`);






-- foreign keys
-- Reference:  `pingresult_ibfk_1` (table: `PINGResults`)


ALTER TABLE `PINGResults` ADD CONSTRAINT `pingresult_ibfk_1` FOREIGN KEY `pingresult_ibfk_1` (`Oid`)
    REFERENCES `FileInfo` (`Id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Reference:  `tcpresult_ibfk_1` (table: `TCPResults`)


ALTER TABLE `TCPResults` ADD CONSTRAINT `tcpresult_ibfk_1` FOREIGN KEY `tcpresult_ibfk_1` (`Oid`)
    REFERENCES `FileInfo` (`Id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- Reference:  `udpresult_ibfk_1` (table: `UDPResults`)


ALTER TABLE `UDPResults` ADD CONSTRAINT `udpresult_ibfk_1` FOREIGN KEY `udpresult_ibfk_1` (`Oid`)
    REFERENCES `FileInfo` (`Id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;



-- End of file.
