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
        self.config["user"] = "Moradster"
        self.config["host"] = "localhost"
        self.config["password"] = "root"
        self.config["database"] = "testdb"
        self.config["autocommit"] = True
    #says config isn't defined. But it is defined at top
    #this doesn't work?
    def connect(self):
        try:
            connect = pymysql.connect(self.config)
            self.cursor = connect.cursor()
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
    
    def __executeQuery(**kwargs):
        lastQuery = kwargs
        try:
            self.cursor.execute(kwargs)
            vtr = self.cursor.fetchall()
            lastResult = vtr
            exeFlag = True
            return (exeFlag, vtr)
        except pymysql.Error as err:
            print (err)
            return False

    def insert(self, table, **kwargs):
        #works for insert purposes
        #need to make a delete function incase of user mistakes
        #make for loop for column check
        columns = __getcolumns(table)
        for row in columns:
            if key in kwargs != columns:
                print("Please enter proper columns and values")
                break
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
        if (query == lastQuery):
            print(lastResult)

        else:
            try:
                __executeQuery(query)
            except pymysql.Error as err:
                print (err)

    def select(self, table, valuesToReturn, *args, **kwargs):
        #need to find a way to find if user input has wrong columns 
        query ="SELECT "
        for keys in args:
            query += "" + keys + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for keys in kwargs:
            query +="" + keys + "%(" + keys + ")s,"
        query = query[:-1]+ ""
        print (query)
        if query == lastQuery:
            print (lastResult)
        else:
            try:
                self.cursor.execute(query, kwargs)
            
            except pymysql.Error as err:
                print (err)
            for item in cursor:
                print (item)

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
userflag = True
while userflag==True:
    x.connect()
    print ("Please select a table to use")
    table = input('--> ')
    columnnames = x.__getcolumns(table)
    print("Would you like to insert information or query table %s?" %table)
    command = input('[Insert/Select]')
    if (command == 'Insert' or command == 'insert'):
        print("['table', column'=string', column'>value', column=integer]")
        insertData = input('—-> ')
        x.insert(insertData)
    if (command == 'Select' or command == 'select'):
        print("['table', 'valuesToReturn', 'column = value']")
        selData = input('--> ')
        x.select(selData)
    else:
        break


