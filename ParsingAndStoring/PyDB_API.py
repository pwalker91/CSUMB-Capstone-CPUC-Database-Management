import pymysql
class CSDI_MySQL():

    lastResult = False
    lastQuery = ""

    config = {}

    def __init__(self):
        self.config = {}
        self.config["user"] = "root"
        self.config["host"] = "localhost"
        self.config["password"] = "thedefault"
        self.config["database"] = "CPUC"
        self.config["autocommit"] = True

    def connect(self):
        try:
            connection = pymysql.connect(**self.config)
            self.cursor = connection.cursor()
            print ("Connection succeeded")
            return True
        except pymysql.Error as err:
            print (err)

    def __checktable(self, table):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        if not tables:
            raise RuntimeError("Something went wrong getting tables")
        tables = [elem[0] for elem in tables]
        return tables

    def __getcolumns(self, table):
        self.cursor.execute("SELECT * FROM %s" %table)
        list = self.cursor.description
        return [getcolm[0] for getcolm in list]

    def __executeQuery(self, query, queryData):
        self.lastQuery = self.__queryAsString(query, queryData)
        try:
            self.cursor.execute(query, queryData)
            self.lastResult = self.cursor.fetchall()
            return (True, self.lastResult)
        except pymysql.Error as err:
            print (err)
            return (False,[])

    def __queryAsString(self, query, queryData):
        queryWithData = query.replace("%(","{").replace(")s","}")
        return queryWithData.format(**queryData)

    def insert(self, table, **kwargs):
        if table not in self.__checktable(table):
            raise ValueError("The given table does not exist")
        columns = self.__getcolumns(table)
        for kwargkey in kwargs:
            if kwargkey not in columns:
                print("Please enter proper columns and values")
                return False
        query = "INSERT INTO " + table + " ("
        for key in kwargs:
            query += "" + key + ","
        query = query[:-1]+" ) VALUES ("
        for key in kwargs:
            query += " %(" + key + ")s,"
        query = query[:-1]+")"
        flag, results = self.__executeQuery(query, kwargs)
        if flag:
            newflag, results = self.__executeQuery("SELECT LAST_INSERT_ID()",[])
            return results[0][0]
        return flag

    def select(self, table, *args, **kwargs):
        if table not in self.__checktable(table):
            raise ValueError("The given table does not exist")
        keys = list(kwargs.keys())
        keys = [elem for elem in keys if "_operator" not in elem]
        query = "SELECT "
        for argkey in args:
            query += "" + argkey + ","
        query = query[:-1] + " FROM " + table + " WHERE "
        for kwargskeys in keys:
            query +=" " + kwargskeys +" "+ kwargs[kwargskeys+ "_operator"] +" %(" + kwargskeys + ")s AND"
        query = query[:-3]+ ""
        if self.__queryAsString(query, kwargs) == self.lastQuery:
            return self.lastResult
        else:
            flag, results = self.__executeQuery(query, kwargs)
            if flag:
                return results

