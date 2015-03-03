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

#IMPORTS
import pymysql

#END IMPORTS


class CSDI_MySQL():

    """
    This class will connect to a specific database, and generate
     queries based on user input
    ATTRIBUTES
        lastResults     List, the returned result from the previous query
        lastQuery       String, the last query executed, with the data inserted
                         into the query
        config          Dictionary, the configuration information for connecting
                         to the database
    """

    #CLASS ATTRIBUTES --------------
    lastResult = False
    lastQuery = ""

    config = {}
    # ------------------------------

    def __init__(self, **kwargs):
        """
        Initializes the object's connection information using kwargs.
        Defaults:
            user:       root
            host:       localhost
            autocommit: True
        """
        #This takes any information in kwargs, and essentially copies it into
        # self.config. As such, you may set config to be anything when you
        # initialize a CSDI_MySQL object
        self.config = {"user": "root",
                       "host": "localhost",
                       "autocommit": True
                       }
        self.config.update(kwargs)
    #END DEF


    #INITIALIZATION ------------------------------------------------------------

    def connect(self):
        """Starts connection and stores le cursor in the object"""
        try:
            connection = pymysql.connect(**self.config)
            self.cursor = connection.cursor()
            print("Connection succeeded")
            return True
        except pymysql.Error as err:
            print(err)
    #END DEF


    #ERROR CHECKING and DECORATORS ---------------------------------------------

    def __checkTable(func):
        def checkTableWrapper(*args, **kwargs):
            """
            Checks if the user's table exists in the database.
             If not, an error is raised
            """
            args[0].cursor.execute("SHOW TABLES")
            tables = args[0].cursor.fetchall()
            if not tables:
                raise RuntimeError("Something went wrong getting tables.")
            tables = [elem[0] for elem in tables]
            if args[1] not in tables:
                raise ValueError("The table you passed in has not been created.")
            return func(*args, **kwargs)
        return checkTableWrapper
    #END DEF

    def __getColumns(self, table):
        """
        Grabs correct columns from database in order to check queries to see
         if any wrong inputs went through
        """
        self.cursor.execute("SHOW COLUMNS FROM %s" %table)
        list = self.cursor.fetchall()
        return [getcolm[0] for getcolm in list]
    #END DEF

    def __executeQuery(self, query, queryData):
        """
        Executes query and saves lastQuery as the query as a string for
         reference use later in insert and select functions
        """
        asString = self.__queryAsString(query, queryData)
        if asString != self.lastQuery:
            self.lastQuery = asString
            try:
                self.cursor.execute(query, queryData)
                self.lastResult = (True, self.cursor.fetchall())
            except pymysql.Error as err:
                print(err)
                self.lastResult = (True, [])
        return self.lastResult
    #END DEF

    def __queryAsString(self, query, queryData):
        """
        Recieves a query with placeholders in it, with the data and
         creates a string version with data in it, for comparison
        """
        queryWithData = query.replace("%(","{").replace(")s","}")
        return queryWithData.format(**queryData)
    #END DEF

    #QUERY GENERATION and EXECUTION --------------------------------------------

    @__checkTable
    def insert(self, table, **kwargs):
        """
        Runs an INSERT query with table and kwargs.
         'table' has the table that user declared, and kwargs is made of
         column/value pairs.
        ARGS:
            table   String, the table to insert into
        **KWARGS:
            key     Dictionary key, the column to insert a value into
            value   String/Integer/Date/Time, the value to insert
        """
        columns = self.__getColumns(table)
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
            newflag, results = self.__executeQuery("SELECT LAST_INSERT_ID()",{})
            return results[0][0]
        return flag
    #END DEF

    @__checkTable
    def select(self, table, *args, **kwargs):
        """
        Creates a simple function using correct tables, columns and values to
         query the database for specific information.
        ARGS:
            table   String, the table to select from
        *ARGS:
            A sequence of Strings, which are the columns from which data should be queried.
            User '*' for all columns
        **KWARGS:
            Key/Value pairs, which represent the column/value pairs in the table
             that form the criteria of the query.
        """
        columns = self.__getColumns(table)
        #kwargs.keys() gets all the key values and puts into a list form
        #the list function is applied to make it mutable
        trueKeys = list(kwargs.keys())
        #add each element from keys to the new array if "_operator" is not in the key name
        #the resulting array is all of the keys in kwargs that are column names
        trueKeys = [elem for elem in trueKeys if "_operator" not in elem]
        for kwargkey in trueKeys:
            if kwargkey not in columns:
                print("Please enter proper columns and values")
                return False
        #This checks that each element in 'args' is a column within the table,
        # or that the argkey is '*'
        if len(args)<1:
            print("You need to pass in what columns you want selected. Pass in '*' for all columns.")
            return False
        for argkey in args:
            if argkey not in columns and argkey != '*':
                print("Please enter proper columns names.")
                return False

        #Adding the columns after SELECT, the columns the user wants returned
        query = "SELECT "
        for argkey in args:
            query += "" + argkey + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for kwargskey in trueKeys:
            #adding to the query what we are looking for
            #kwarg key = column name, kwargs[kwargskeys + _operator] is grabbing the mathematical operator from kwargs
            #kwargskeys is being used as a placeholder in query string
            query +=" " + kwargskey +" "+ kwargs[kwargskey+"_operator"] +" %(" + kwargskey + ")s AND"
        query = query[:-3]+ ""
        return self.__executeQuery(query, kwargs)
    #END DEF
#END CLASS
