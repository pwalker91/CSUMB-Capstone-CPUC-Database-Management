import pymysql
###this works just as well as import mysql.connector
#For this i am assuming that this script will be called?
#or is it being ran from main?
#nick has questions about variables lastResult and lastQuery and functions connect() and config (param, param)
class CSDI_MySQL():

    lastResult = False
    lastQuery = ""

    config = {}
 
 
    def __init__(self):
        #defines config data
        #does this need to be user input?
        self.config = {}
        self.config["user"] = "Moradster"
        self.config["host"] = "localhost"
        self.config["password"] = "root"
        self.config["database"] = "testdb"
        self.config["autocommit"] = True
    #says config isn't defined. But it is defined at top
    #this doesn't work?
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
        #works for insert purposes
        #need to make a delete function incase of user mistakes
        #make for loop for column check
        columns = self.__getcolumns(table)
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
        keys = list(kwargs.keys())
        keys = [elem for elem in keys if "_operator" not in elem]
        
        query ="SELECT "
        for argkey in args:
            query += "" + argkey + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for kwargskeys in keys:
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


