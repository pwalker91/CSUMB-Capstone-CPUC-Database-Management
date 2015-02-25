
"""-------------------------------------------------------------------------------
        """
import pymysql
class CSDI_MySQL():

    lastResult = False
    lastQuery = ""

    config = {}
 
 
    def __init__(self):

        self.config = {}
        self.config["user"] = "Moradster"
        self.config["host"] = "localhost"
        self.config["password"] = "root"
        self.config["database"] = "testdb"
        self.config["autocommit"] = True

    def connect(self):
        try:
            connection = pymysql.connect(**self.config)
            self.cursor = connection.cursor()
            print ("Connection succeeded")
            return True
        except pymysql.Error as err:
            print (err)
    #def config(self, configDictionary, **kwargs):
    #gets columns to compare
    def __getcolumns(self, table):
        self.cursor.execute("SELECT * FROM %s" %table)
        #used to grab column data
        list = self.cursor.description
        #returns the first item (column name) in each tuple
        return [getcolm[0] for getcolm in list]
    
    def __executeQuery(self, query, queryData):
        self.lastQuery = query
        try:
            self.cursor.execute(query, queryData)
            vtr = self.cursor.fetchall()
            self.lastResult = vtr
            return (True, vtr)
        except pymysql.Error as err:
            print (err)
            return (False,[])

    def insert(self, table, **kwargs):
        columns = self.__getcolumns(table)
        #Grabing every key in kwargs assigning to kwargkey
        #Check to see if value kwargkey is in columns
        for kwargkey in kwargs:
            if kwargkey not in columns:
                print("Please enter proper columns and values")
                return False
        self.cursor.execute("SELECT * FROM %s" %table)
        query = "INSERT INTO " + table + " ("
        for key in kwargs:
            query += "" + key + ","
        query = query[:-1]+" ) VALUES ("
        for key in kwargs:
            query += " %(" + key + ")s,"
        query = query[:-1]+")"
        #print (query)
        #print (kwargs)
        if (query == self.lastQuery):
            print(self.lastResult)

        else:
            try:
                self.__executeQuery(query, kwargs)
            except pymysql.Error as err:
                print (err)

    def select(self, table, *args, **kwargs):
        #need to find a way to find if user input has wrong columns
        columns = self.__getcolumns(table)
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
        query ="SELECT "
        for argkey in args:
            query += "" + argkey + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for kwargskeys in keys:
            #adding to the query what we are looking for
            #kwarg key = column name, kwargs[kwargskeys + _operator] is grabbing the mathematical operator from kwargs
            #kwargskeys is being used as a placeholder in query string
            query +=" " + kwargskeys +" "+ kwargs[kwargskeys+ "_operator"] +" %(" + kwargskeys + ")s AND"
        query = query[:-3]+ ""
        print (query)
        if query == self.lastQuery:
            print(self.lastResult)
        else:
            try:
                flag,results = self.__executeQuery(query, kwargs)
                print (results)
            except pymysql.Error as err:
                print (err)
        #just in case.....
    """def update(self,table, *args, **kwargs):
        query = "UPDATE " + table + " SET "
        for key in args:
            query += "" + key + ","
        query = query[:-1]+" WHERE "
        for key in kwargs:
            query += "" + key + " =%("+ key + ")s,"
        query = query[:-1]
        print (query)
        try:
            self.cursor.execute(query, kwargs)
            for row in cursor:
                print (row)
        except pymysql.Error as err:
            print (err)"""

x = CSDI_MySQL()
x.connect()
x.select("test", "*" ,
         speed_operator='>', speed='4',
         id_operator='=', id='6',
         provider_operator='LIKE', provider='t%',
         date_operator='<', date='2015-02-15')
x.insert("test", speed ='5.7', id = '10', provider = 'sprint', date = '2015-02-20')



"""want query like: 
    kwargs = {data = "hi", data_operator = "Some operator <,>"
    query += ""+keys+"" + " "+kwargs[keys+"_operator"] + .... """


