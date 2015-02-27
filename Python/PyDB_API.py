"""
-------------------------------------------------------------------------------
PyDB_API.PY

AUTHOR(S):  Peter Walker: pwalker@csumb.edu
            Nicholas Moradi: nmoradi@csumb.edu

PURPOSE-  This module will be used for data manipulation in MySQL Databases.
            Ability to SELECT and INSERT. Creates a class that will use multiple
            functions to do what it needs to do.

CLASSES-
    CSDI_MySQL
        CLASS VARIABLES-
            lastResult = False
            lastQuery = ""
            config = {}
        FUNCTIONS-
            __init__(self)
            connect(self)
            insert(self, table **kwargs)
            select(self, table, *args, **kwargs)
-------------------------------------------------------------------------------
"""

import pymysql
class CSDI_MySQL():
    """
    This class will connect to a specific database, and generate
     queries based on user input
    """
    lastResult = False
    lastQuery = ""

    config = {}

    def __init__(self):
        """
        Initializes the object's connection information
        """
        self.config = {}
        self.config["user"] = "root"
        self.config["host"] = "localhost"
        self.config["password"] = "thedefault"
        self.config["database"] = "CPUC"
        self.config["autocommit"] = True
    #connects to mysql db
    def connect(self):
        """
        Starts connection and stores le cursor in the object
        """
        try:
            connection = pymysql.connect(**self.config)
            self.cursor = connection.cursor()
            print ("Connection succeeded")
            return True
        except pymysql.Error as err:
            print (err)
    #compares table input to actual tables
    def __checktable(self, table):
        """
        Checks if the user's table exists in the database. If not an error is returned
        """
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        if not tables:
            raise RuntimeError("Something went wrong getting tables")
        tables = [elem[0] for elem in tables]
        return tables
    #gets columns to compare queries too
    def __getcolumns(self, table):
        """
        Grabs correct columns from database in order to check queries to see if any wrong inputs went through
        """
        self.cursor.execute("SHOW COLUMN FROM %s" %table)
        list = self.cursor.description
        return [getcolm[0] for getcolm in list]

    def __executeQuery(self, query, queryData):
        """
            Executes query and saves lastQuery as the query as a string for reference use later in insert and select functions
        """
        self.lastQuery = self.__queryAsString(query, queryData)
        try:
            self.cursor.execute(query, queryData)
            self.lastResult = self.cursor.fetchall()
            return (True, self.lastResult)
        except pymysql.Error as err:
            print (err)
            return (False,[])

    def __queryAsString(self, query, queryData):
        """Recieves a query with placeholders in it, with the data and creates a string version with data in it, for comparison
        """
        queryWithData = query.replace("%(","{").replace(")s","}")
        return queryWithData.format(**queryData)

    def insert(self, table, **kwargs):
        """Runs an INSERT query with table and kwargs.
            Table has the table that user declared. Table to be checked
            KWARGS:
                we expect in kwargs:
                    Location = '[input]', DeviceID = '[input]'
                    In this example DeviceID and Location would be keys within in kwargs and would be paired the inputs which are either strings or numbers. These inputs are the values we would be inserting into the row.         """
        if table not in self.__checktable(table):
            raise ValueError("The given table does not exist")
        columns = self.__getcolumns(table)
        #Grabing every key in kwargs assigning to kwargkey
        #Check to see if value kwargkey is in columns
        for kwargkey in kwargs:
            if kwargkey not in columns:
                print("Please enter proper columns and values")
                return False
        query = "INSERT INTO " + table + " ("
        for key in kwargs:
            query += "" + key + ","
        query = query[:-1]+" ) VALUES ("
        for key in kwargs:
            query += " %(" + key + ")s,"
        query = query[:-1]+")"
        flag, results = self.__executeQuery(query, kwargs)
        if flag:
            newflag, results = self.__executeQuery("SELECT LAST_INSERT_ID()",[])
            return results[0][0]
        return flag

    def select(self, table, *args, **kwargs):
        """
        Creates a simple function using correct tables, columns and values to query the database for specific information.
            TABLE: Table inputed, still needs to be checked by function
            ARGS: This holds all of the column names describing the values to be returned
            KWARGS: Hold the values for the specific columns to be searched for
        """
        if table not in self.__checktable(table):
            raise ValueError("The given table does not exist")
        columsn = self.getcolumns(table)
        for kwargkey in kwargs:
            if kwargkey not in columns:
                print("Please enter proper columns and values")
                return False
            #kwargs.keys() gets all the key values and puts into a list form
            #the list function is applied to make it mutable
        keys = list(kwargs.keys())
        #add each element from keys to the new array if "_operator" is not in the key name
        #the resulting array is all of the keys in kwargs that are column names
        keys = [elem for elem in keys if "_operator" not in elem]
        query = "SELECT "
        for argkey in args:
            query += "" + argkey + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for kwargskeys in keys:
            #adding to the query what we are looking for
            #kwarg key = column name, kwargs[kwargskeys + _operator] is grabbing the mathematical operator from kwargs
            #kwargskeys is being used as a placeholder in query string
            query +=" " + kwargskeys +" "+ kwargs[kwargskeys+ "_operator"] +" %(" + kwargskeys + ")s AND"
        query = query[:-3]+ ""
        if self.__queryAsString(query, kwargs) == self.lastQuery:
            return self.lastResult
        else:
            flag, results = self.__executeQuery(query, kwargs)
            if flag:
                return results

