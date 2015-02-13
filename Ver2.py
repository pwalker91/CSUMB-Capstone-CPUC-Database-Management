config = {}
def __init__(self):
    config["user"] = "Moradster"
    config["host"] = "localhost"
    config["password"] = "root"
    config["database"] = "testdb"
    config["autocommit"] = True
    
    
    #gets columns to compare
def _getcolumns(table):
    cursor.execute("SELECT * FROM %s" %table)
        #used to grab column data
    list = cursor.description
        #returns the first item (column name) in each tuple
    return [getcolm[0] for getcolm in list]

    #insert works!
def insert(cursor, table, **kwargs):
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

    query ="SELECT "
    for keys in kwargs:
        query += "" + keys + ","
    query = query[:-1] + "FROM " + table + "WHERE "
    for keys in kwargs:
        query += " %(" + key + ")s,"
    query = query[:-1]+ ""
    print (query)



def update(cursor, table, **kwargs):
    query = "UPDATE " + table + "SET "
    for key in kwargs:
        query += "" + key + ","
    query = query[:-1]+" WHERE "
    for key in kwargs:
        query += "" + key + " = %("+ key + ")s,"
    query = query[:-1]
    print (query)

import pymysql
###this works just as well as import mysql.connector
connect = pymysql.connect(host='localhost', user='Moradster', password='root', database='testdb', autocommit= True)
cursor = connect.cursor()
cursor.execute("SHOW TABLES")
print ("Please select a table to use")
table = input('--> ')
print("Would you like to insert information, query or update table %s?" %table)
iorq = input('i/q/u: ')
if iorq == 'i' or iorq == 'I':
    insert(cursor, table, id='7', date='2015-6-5', provider= 't-mobile', speed='8.4')
if iorq == 'q' or iorq == 'Q':
    select(cursor, table, id, speed='4.5')
if iorq == 'u' or iorq =='U':
    update(cursor, table, """<orginal column name> = <ori value>, <new/old column> = <new value>""")
elif iorq != 'q' or iorq != 'i' or iorq != 'u':
        userflag = False



