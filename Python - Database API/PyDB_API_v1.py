#import pymysql
import pymysql
###this works just as well as import mysql.connector
connect = pymysql.connect(host='localhost', user='Moradster', password='root', database='testdb', autocommit= True)
cursor = connect.cursor()
userflag = True
"""def test_func(var1, *args, **kwargs):
    print (var1)
    print (args)
    print (kwargs)
#test_func()
test_func(1, "a", "b", ui=13, passs="hello")"""
def getcolumns(table):
    cursor.execute("SELECT * FROM %s" %table)
    #used to grab column data
    list = cursor.description
    #returns the first item (column name) in each tuple
    return [getcolm[0] for getcolm in list]
#def update_table(table, columns):
    

def insert_into(table, **kwargs):
    cursor.execute("SELECT * FROM %s" %table)
    """values = []
    valueids = ()
    for items in columns:
        values.append(input('--> '))
    columnids = ", ".join(columns)
    for items in values:
        val_index = values.index(items)
        values[val_index] = "'" + str(items) + "',"
    valueids = ",".join(values)
    print(valueids)"""

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

    #need to find a way to pull string from lists without manually doing it
    #this should work but doesn't
    #cursor.execute("INSERT INTO %s (%s, %s, %s, %s) VALUES ('%d', '%s','%s','%f')")
    #another failed attempt
    #cursor.execute("INSERT INTO ", table, "(", columns, ") VALUES (", values, ")")
    #closest so far
    #cursor.execute("INSERT INTO %s (%s) VALUES (%s)" %(table, columnids, valueids)
    return userflag == True


#This function asks for user input in order to form a query
#Don't know to make it automated
#Trying to figure out how to make it automated
#This works as long as user understands table structure and schema
def select_from(table, columns):
    cursor.execute("SELECT * FROM %s" %table)
    for row in cursor:
        print (row)
    #added for cases where WHERE is used to query
    print("Would you like to be more specific? :")
    yn = input('Y/N: ')
    if yn == 'n' or yn == 'N':
        print("Goodbye")
    elif yn == 'y' or yn == 'Y':
        #selects column to look for
        print("Select a column you would like to query from %s: " %(columns))
        column_id = input('--> ')
        #gets value of the column
        print("Please add value to search column %s: " %column_id)
        valueid = input('--> ')
        #type of mathemathics applied to the value =, <, >
        #more of these types of operands can be allowed => and =<
        print("Please insert type of function for value: \n"
              "1. Equal to \n"
              "2. Greater than \n"
              "3. Less than ")
        func = input('--> ')
        #form successful query based off of information provided.
        if func == '1':
            cursor.execute("SELECT * FROM %s WHERE %s ='%s'" %(table, column_id, valueid))
            for row in cursor:
                print (row)
        if func == '2':
            cursor.execute("SELECT * FROM %s WHERE %s >'%s'" %(table, column_id, valueid))
            for row in cursor:
                print (row)
        if func == '3':
            cursor.execute("SELECT * FROM %s WHERE %s <'%s'" %(table, column_id, valueid))
            for row in cursor:
                print (row)
        return userflag == True


#def update(table,):
#set to connect to my mysql db
#shows tables available to query
while userflag == True:
    cursor.execute("SHOW TABLES")
    for row in cursor:
        print (row)
    print("Select a table to query: ")
    table_input = input('--> ')
    columnlist = getcolumns(table_input)
    columnlength = len(columnlist)
    print ("Columns: \n"
           "%s"  %columnlist)
    #if insert different function would be called
    #if query generic query made: SELECT * FROM <table> where <columnid> = <value>
    print("Would you like to insert information, query or update table %s?" %table_input)
    iorq = input('i/q/u: ')
    if iorq == 'i' or iorq == 'I':
        insert_into(table_input, id='6', date='2015-2-5', provider= 'att', speed='4.5')
    if iorq == 'q' or iorq == 'Q':
        select_from(table_input, columnlist)
    elif iorq != 'q' or iorq != 'i' or iorq != 'u':
        userflag = False

cursor.close()
connect.close()