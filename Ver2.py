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

def insert(cursor, table, **kwargs):
    #works for insert purposes
    #need to make a delete function incase of user mistakes
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

def select(cursor, table, *args, **kwargs):
    #works minimally
    query ="SELECT "
    for keys in args:
        query += "" + keys + ","
    query = query[:-1] + " FROM " + table + " WHERE "
    for keys in kwargs:
        query +="" + keys + "=%(" + keys + ")s,"
    query = query[:-1]+ ""
    print (query)
    cursor.execute(query, kwargs)
    for row in cursor:
        print (row)
    return userflag == True



def update(cursor, table, *args, **kwargs):
    query = "UPDATE " + table + "SET "
    for key in kwargs:
        query += "" + key + ","
    query = query[:-1]+" WHERE "
    for key in kwargs:
        query += "" + key + " =%("+ key + ")s,"
    query = query[:-1]
    print (query)
#class myAPI():
#place correctly working select, insert and update mysql commands here


import pymysql
###this works just as well as import mysql.connector
connect = pymysql.connect(host='localhost', user='Moradster', password='root', database='testdb', autocommit= True)
userflag = True
while userflag==True:
    cursor = connect.cursor()
    cursor.execute("SHOW TABLES")
    for items in cursor:
        print(items)
    print ("Please select a table to use")
    table = input('--> ')
    print("Would you like to insert information, query or update table %s?" %table)
    iorq = input('i/q/u: ')
    if iorq == 'i' or iorq == 'I':
        insert(cursor, table, id='7', date='2015-6-5', provider= 't-mobile', speed='8.4')
    if iorq == 'q' or iorq == 'Q':
        select(cursor, table, 'id', speed='5')
    if iorq == 'u' or iorq =='U':
        update(cursor, table, """<orginal column name> = <ori value>, <new/old column> = <new value>""")
    elif iorq != 'q' or iorq != 'i' or iorq != 'u':
        userflag == False
        break



