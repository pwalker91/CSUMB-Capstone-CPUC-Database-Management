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
    lastResult = (False,[])
    lastQuery = ""

    config = {}
    cursor = None
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
        self.cursor = None
    #END DEF

    def __del__(self):
        """Safely destroys the object, closing database connections"""
        self.config = {}
        if isinstance(self.cursor, pymysql.cursors.Cursor.__class__):
            self.cursor.close()
        self.cursor = None
        print("Database connection closed.")
    #END DEF


    #INITIALIZATION ------------------------------------------------------------

    def connect(self):
        """Starts connection and stores le cursor in the object"""
        if 'database' not in self.config:
            print("You must specify a database before you can connect.")
            return False
        #Now that we know self.config['database'] is set, we try connecting
        try:
            connection = pymysql.connect(**self.config)
            self.cursor = connection.cursor()
            print("Connection established to {}.".format(self.config['database']))
            return True
        except pymysql.Error as err:
            print(err)
            return False
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

    def __checkColumns(func):
        def checkColumnsWrapper(*args, **kwargs):
            """
            Checks the given columns in args and kwargs, and if the tables exist
             in the given table.
            """
            args[0].cursor.execute("SHOW COLUMNS FROM {}".format(args[1]))
            columnsList = [column[0] for column in args[0].cursor.fetchall()]
            givenColumns = list(args[2:])
            if "*" in givenColumns:
                givenColumns.remove(givenColumns.index("*"))
            [givenColumns.append(key) for key in kwargs if "_operator" not in key]
            for column in givenColumns:
                if column not in columnsList:
                    raise RuntimeError("The given column, '{}'".format(column)+
                                       ", is not in the given table, '{}'".format(args[1]))
            return func(*args, **kwargs)
        return checkColumnsWrapper
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
                self.lastResult = (False, self.lastResult[-1])
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

    @__checkColumns
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
        query = "INSERT INTO {} (".format(table)
        for key in kwargs:
            query += "{}, ".format(key)
        query = query[:-2]+" ) VALUES ("
        for key in kwargs:
            query += "%({})s, ".format(key)
        query = query[:-2]+")"
        flag, results = self.__executeQuery(query, kwargs)
        if flag:
            newflag, results = self.__executeQuery("SELECT LAST_INSERT_ID()",{})
            return results[0][0]
        return flag
    #END DEF

    @__checkColumns
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
            Key/operator pairs, where the key is the column name, followed
             by '_operator'. This can be '=', '>', etc.
            The only conjunction available is 'AND'. If you wish to execute a
             more selective query, you must call executeAQuery().
        """
        #kwargs.keys() gets all the key values from kwargs, and puts into a list form.
        #The list function is applied to make it mutable
        #We then add each element from the keys to the new array if "_operator"
        # is not in the key name. The resulting array is all of the keys in
        # kwargs that are column names.
        trueKeys = [elem for elem in list(kwargs.keys()) if "_operator" not in elem]
        #This checks that each element in 'args' is a column within the table,
        # or that the argkey is '*'
        if len(args)<1:
            raise RuntimeError("You need to pass in what columns you want selected."+
                               "Pass in '*' for all columns.")

        #Adding the columns after SELECT, the columns the user wants returned
        query = "SELECT "
        for argkey in args:
            query += "{}, "
        query = query[:-2] + " FROM {} WHERE ".format(table)
        for kwargskey in trueKeys:
            #adding to the query what we are looking for
            #kwarg key = column name, kwargs[kwargskey + _operator] is grabbing
            # the mathematical operator from kwargs
            #kwargskey is being used as a placeholder in query string
            acceptableOps = ["=", "<>", ">", ">=", "<", "<="]
            if kwargskey+"_operator" not in kwargs:
                kwargs[kwargskey+"_operator"] = "="
            else:
                if kwargs[kwargskey+"_operator"] not in acceptableOps:
                    print("You gave an incorrect SQL predicate. "+
                          "Was given '{}'".format(kwargs[kwargskey+"_operator"]))
                    return self.lastResult
            #END IF/ELSE

            #Now we actually create the criteria, subbing in the column name,
            # operator, and conjunction
            query +=" {} {} %({})s AND".format(kwargskey,
                                               kwargs[kwargskey+"_operator"],
                                               kwargskey)
        #Removing the AND from the end of our query
        query = query.rsplit(" ",1)[0]
        return self.__executeQuery(query, kwargs)
    #END DEF


    def _executeAQuery(self, *args, **kwargs):
        return False
    #END DEF
#END CLASS
