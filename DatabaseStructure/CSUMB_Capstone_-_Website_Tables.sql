-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Fri Mar 20 05:47:54 UTC 2015




-- tables
-- Table HelpRequest
CREATE TABLE HelpRequest (
    Id smallint    NOT NULL ,
    InsertTimestamp timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ,
    Name varchar(50)    NULL ,
    Email varchar(50)    NOT NULL ,
    Subject varchar(30)    NOT NULL ,
    Message blob    NOT NULL ,
    PhoneNumber varchar(20)    NULL ,
    LastPageVisited varchar(50)    NOT NULL ,
    CONSTRAINT HelpRequest_pk PRIMARY KEY (Id)
) ENGINE INNODB
;

-- Table Query
CREATE TABLE Query (
    Id int    NOT NULL ,
    InsertTimestamp timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP ,
    AnalysisOpts blob    NOT NULL ,
    ContactEmail varchar(50)    NOT NULL ,
    ContactName varchar(50)    NULL ,
    IsGenerated bool    NOT NULL ,
    ErrorEncountered bool    NOT NULL ,
    CONSTRAINT Query_pk PRIMARY KEY (Id)
) ENGINE INNODB
;

-- Table Results
CREATE TABLE Results (
    Id int    NOT NULL ,
    CalculatedData blob    NOT NULL ,
    ImagePath varchar(100)    NOT NULL ,
    MetaInfo blob    NOT NULL ,
    PageHash varchar(10)    NOT NULL ,
    CONSTRAINT Results_pk PRIMARY KEY (Id)
) ENGINE INNODB
;





-- foreign keys
-- Reference:  FK_0 (table: Results)


ALTER TABLE Results ADD CONSTRAINT FK_0 FOREIGN KEY FK_0 (Id)
    REFERENCES Query (Id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;



-- End of file.

