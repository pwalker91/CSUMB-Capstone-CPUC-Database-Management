import pymysql
###this works just as well as import mysql.connector
class myAPI():
    def __init__(self):
        config ={}
        config["user"] = "Moradster"
        config["host"] = "localhost"
        config["password"] = "root"
        config["database"] = "testdb"
        config["autocommit"] = True
        connect = pymysql.connect(**config)
        self.cursor = connect.cursor()
    
    
    #gets columns to compare
    def _getcolumns(self, table):
        self.cursor.execute("SELECT * FROM %s" %table)
        #used to grab column data
        list = cursor.description
        #returns the first item (column name) in each tuple
        return [getcolm[0] for getcolm in list]

    def insert(self, table, **kwargs):
        #works for insert purposes
        #need to make a delete function incase of user mistakes
        #print (pymysql.Error as err)
        self.cursor.execute("SELECT * FROM %s" %table)
        query = "INSERT INTO " + table + " ("
        for key in kwargs:
            query += "" + key + ","
        query = query[:-1]+" ) VALUES ("
        for key in kwargs:
            query += " %(" + key + ")s,"
        query = query[:-1]+")"
        print (query)
        print (kwargs)
        try:
            self.cursor.execute(query, kwargs)
        except pymysql.Error as err:
            print (err)

    def select(self, table, *args, **kwargs):
        #works minimally
        query ="SELECT "
        for keys in args:
            query += "" + keys + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for keys in kwargs:
            query +="" + keys + "=%(" + keys + ")s,"
        query = query[:-1]+ ""
        print (query)
        try:
            self.cursor.execute(query, kwargs)
        except pymysql.Error as err:
            print (err)
        for item in cursor:
            print (item)

    def update(self,table, *args, **kwargs):
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
            print (err)

x = myAPI()
userflag = True
while userflag==True:
    x.cursor.execute("SHOW TABLES")
    for items in x.cursor:
        print(items)
    print ("Please select a table to use")
    table = input('--> ')
    print("Would you like to insert information, query or update table %s?" %table)
    iorq = input('i/q/u: ')
    if iorq == 'i' or iorq == 'I':
        x.insert(table, id='8', date='2015-2-15', provider='sprint', speed='8.3')
    if iorq == 'q' or iorq == 'Q':
        select(table, 'id', 'date', speed='5')
    if iorq == 'u' or iorq =='U':
        update(table, "date = '2015-2-15'", id= '6')
    elif iorq != 'q' or iorq != 'i' or iorq != 'u':
        userflag == False
        break



