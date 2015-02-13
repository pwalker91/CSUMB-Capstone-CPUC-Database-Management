class API():
    def __init__(self):
        self.data = []
    def _getcolumns(table):
        cursor.execute("SELECT * FROM %s" %table)
        #used to grab column data
        list = cursor.description
        #returns the first item (column name) in each tuple
        return [getcolm[0] for getcolm in list]

    def insert(cursor, table, **kwargs):
        columnList = _getcolumns(table)
        for item in columnList:
            if columnList[item] != kwargs[item]:
                print ("Exiting")
        #print (pymysql.Error as err)
        cursor.execute("SELECT * FROM %s" %table)
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
            cursor.execute(query, kwargs)
        except pymysql.Error as err:
            print (err)

    def select(cursor, table, **kwargs):
        columnList = _getcolumns(table)
        for items in columnList:
            if columnList[items] != kwargs[items]:
                print ("Exiting")
        #print (pymysql.Error as err)
        query ="SELECT"
        for keys in kwargs:
            query += "" + keys + ","
        query = query[:-1] + "FROM " + table + "WHERE "
        for keys in kwargs:
            query += " %(" + key + ")s,"
        query = query[:-1]+ ")"
        print (query)
                 
                 
import pymysql
###this works just as well as import mysql.connector
connect = pymysql.connect(host='localhost', user='Moradster', password='root', database='testdb', autocommit= True)
cursor = connect.cursor()



