"""
--------------------------------------------------------------------------------
PyDB_API.PY

AUTHOR(S):  Peter Walker        pwalker@csumb.edu
            Nicholas Moradi     nmoradi@csumb.edu

PURPOSE-  This module will be used for data manipulation in MySQL Databases.
            Ability to SELECT and INSERT. Creates a class that will use multiple
            functions to do what it needs to do.
--------------------------------------------------------------------------------
"""

#IMPORTS
import pymysql
#END IMPORTS


class CSDI_MySQL(object):

    """
    This class will connect to a specific database, and generate
     queries based on user input
    ATTRIBUTES
        lastResults     List, the returned result from the previous query
        lastQuery       String, the last query executed, with the data inserted
                         into the query
        config          Dictionary, the configuration information for connecting
                         to the database
        connection      PyMySQL Connection object
        cursor          PyMySQL Cursor object
    """

    #CLASS ATTRIBUTES --------------
    lastResult = (False,[])
    lastQuery = ""

    config = {}
    connection = None
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
        if isinstance(self.connection, pymysql.connections.Connection.__class__):
            self.connection.close()
        self.connection = None
        self.cursor = None
        print("Database connection closed.")
    #END DEF


    #INITIAL CONNECT -----------------------------------------------------------

    def connect(self):
        """Starts connection and stores le cursor in the object"""
        if 'database' not in self.config:
            print("You must specify a database before you can connect.")
            return False
        #Now that we know self.config['database'] is set, we try connecting
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
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
                raise ValueError("The table '{}' has not been created.".format(args[1]))
            return func(*args, **kwargs)
        return checkTableWrapper
    #END DEF

    def __checkTableAlt(self, query):
        """
        This function takes a query string, and splits the table name from it.
         It then checks that this table has been created within the database.
        """
        tableName = query.lower().split("from ")[1].split(" ")[0]
        if not tableName:
            raise ValueError("Your query must contain a table name. Please check your query at \n"+
                             "'{}'".format(query[query.lower().index("from")+4:]))
        #Now that we know we passed the IF block, and so some kind of data must be in tableName
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        if not tables:
            raise RuntimeError("Something went wrong getting tables.")
        tables = [elem[0] for elem in tables]
        if tableName not in tables:
            raise ValueError("The table '{}' has not been created.".format(tableName))
        return True
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
                givenColumns.remove("*")
            [givenColumns.append(key) for key in kwargs if "_COMP" not in key]
            for column in givenColumns:
                if column not in columnsList:
                    raise RuntimeError("The given column, '{}'".format(column)+
                                       ", is not in the given table, '{}'".format(args[1]))
            return func(*args, **kwargs)
        return checkColumnsWrapper
    #END DEF

    def __checkConnected(func):
        def checkConnectedWrapper(*args, **kwargs):
            if not args[0].connection or not args[0].cursor:
                raise RuntimeError("You must be connected to a data to execute this query.")
            return func(*args, **kwargs)
        return checkConnectedWrapper
    #END DEF


    # HIDDEN FUNCTIONS FOR EXECUTING QUERIES -----------------------------------

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
                #This block will first get all of the results. But we are not sure if the
                # user knows the order in which the columns are, so we want to insert
                # the column names in front of the results returned
                #Making sure that we have column names (ie. cursor.description is not None)
                if self.cursor.description:
                    #Getting the first element from each item in cursor.description
                    columnsReturned = tuple( [columnInfo[0] for columnInfo in self.cursor.description] )
                    allResults = list(self.cursor.fetchall())
                    allResults.insert(0, columnsReturned)
                    self.lastResult = (True, tuple(allResults))
                else:
                    self.lastResult = (True, ())
            except pymysql.Error as err:
                print(err)
                print("QUERY: '{}'".format(asString))
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

    @__checkConnected
    @__checkTable
    @__checkColumns
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
        RETURNS:
            BOOLEAN or INT. False on failure, or the row ID of the new row inserted
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
            return self.cursor.lastrowid
        return flag
    #END DEF

    @__checkConnected
    @__checkTable
    @__checkColumns
    def select(self, table, *args, **kwargs):
        """
        Creates a simple function using correct tables, columns and values to
         query the database for specific information.
        !!!
        Note that you do not have control of the order in which the columns are
         added to the query. You must assume that the columns given in kwargs
         and args will not be int he order you specify them. You can also not
         change the conjuntion between AND and OR
        !!!
        ARGS:
            table   String, the table to select from
        *ARGS:
            A sequence of Strings, which are the columns from which data should be queried.
            User '*' for all columns
        **KWARGS:
            Key/Value pairs, which represent the column/value pairs in the table
             that form the criteria of the query.
            Key/operator pairs, where the key is the column name, followed
             by '_COMP'. This can be '=', '>', etc.
            The only conjunction available is 'AND'. If you wish to execute a
             more selective query, you must call _executeAQuery().
        RETURNS:
            The results of the query executing. These will be a tuple, containing:
             BOOLEAN        - Whether the given query was able to execute correctly
             pymysql RESULT - Which itself contains an array of...
                Tuple of column headers (Strings)
                Tuples of results (in the order specified by the column headers)
        """
        #kwargs.keys() gets all the key values from kwargs, and puts into a list form.
        #The list function is applied to make it mutable
        #We then add each element from the keys to the new array if "_COMP"
        # is not in the key name. The resulting array is all of the keys in
        # kwargs that are column names.
        trueKeys = [elem for elem in list(kwargs.keys()) if "_COMP" not in elem]
        #This checks that each element in 'args' is a column within the table,
        # or that the argkey is '*'
        if len(args)<1:
            raise RuntimeError("You need to pass in what columns you want selected."+
                               "Pass in '*' for all columns.")

        #Adding the columns after SELECT, the columns the user wants returned
        query = "SELECT "
        #If the user wants all columns, then we only want to use the "*", otherwise,
        # append each column name
        if "*" in args:
            query += "*, "
        else:
            for argkey in args:
                query += "{}, ".format(argkey)
        #END IF/ELSE
        query = query[:-2] + " FROM {} WHERE ".format(table)
        #If no ops were given, then we just want to query everything
        if len(kwargs)==0:
            query += "1=1"
        else:
            for kwargskey in trueKeys:
                #adding to the query what we are looking for
                #kwarg key = column name, kwargs[kwargskey + _COMP] is grabbing
                # the mathematical operator from kwargs
                #kwargskey is being used as a placeholder in query string
                acceptableOps = ["=", "<>", ">", ">=", "<", "<="]
                if kwargskey+"_COMP" not in kwargs:
                    kwargs[kwargskey+"_COMP"] = "="
                else:
                    if kwargs[kwargskey+"_COMP"] not in acceptableOps:
                        print("You gave an incorrect SQL predicate. "+
                              "Was given '{}'".format(kwargs[kwargskey+"_COMP"]))
                        return self.lastResult
                #END IF/ELSE

                #Now we actually create the criteria, subbing in the column name,
                # operator, and conjunction
                query +=" {} {} %({})s AND".format(kwargskey,
                                                   kwargs[kwargskey+"_COMP"],
                                                   kwargskey)
            #Removing the AND from the end of our query
            query = query.rsplit(" ",1)[0]
        #END IF/ELSE
        return self.__executeQuery(query, kwargs)
    #END DEF


    def _executeQuery(self, *args, **kwargs):
        """
        A function for sending queries to the SQL database. You must use either
         *args or **kwargs, no combination of the two.
        ARGS/KWARGS:
            args[0] or kwargs['query']
                The SQL query you wish to execute
            args[1] or kwargs['queryData']
                The data you wish to send with the SQL query. Must be in a dictionary.
                 Can be empty, or not exist. If it does not exist, then the data
                 is assumed to already exist within the query.
                If you wish to send the query with data, be sure that the query
                 has the appropiate placeholder values, and that each placholder
                 has a corresponding key in the query data dictionary
        """
        #Initial variable declaration
        if len(args):
            query = args[0]
            queryData = args[1]
        else:
            if 'query' not in kwargs:
                raise ValueError("You must pass a query in through the keyword argument 'query'.")
            query = kwargs['query']
            if 'queryData' not in kwargs:
                queryData = {}
            else:
                queryData = kwargs['queryData']
        #END IF/ELSE
        if not isinstance(query, str):
            raise ValueError("You must pass in a query as a string. Was given {}".format(type(query)))
        if not isinstance(queryData, dict):
            raise ValueError("You must pass in query data as a dictionary. Was given {}".format(type(queryData)))
        #The last thing we do before we send the query is check that a table has been given, and
        # then check that each key in queryData has a matching placeholder in the query.
        self.__checkTableAlt(query)
        for key in queryData:
            if key not in query:
                raise ValueError("Some data that you gave does not have a placeholder in the SQL query.\n"+
                                 "The item '{}' is missing a placeholder in the query".format(key))
        #Calling execute, returning the result
        return self.__executeQuery(query, queryData)
    #END DEF
#END CLASS
