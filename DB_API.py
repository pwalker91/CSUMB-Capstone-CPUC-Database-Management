# DESC: Given a query string (and optionally the placeholder data in query_data), will execute the query
#       using the connection made and stored in this object. Will return values pertaining to the query passed
def _executeQuery(self, query, query_data=None):
    #We first check that the variables passed to use are a legitimate MySQL Connection
    # and a MySQL Cursor. Also makes sure that autocommit it True.
    if not isinstance(self._connection, MySQL.connection.MySQLConnection): self.connect()
    #Next check that the query passed is a string
    if not isinstance(query, str): raise TypeError("The query passed must be a string")
    #Checking that the query data is passed as a dictionary
    if query_data and not (isinstance(query_data, dict) or isinstance(query_data, list)):
        raise TypeError("The query data passed must be a dictionary or list")
    #Now we split the query based on the ";" character, and use just the first element.
    # If there was only one query, with or without the ";", then that will be used
    query = query.split(";")[0]

    #Now we run the query with our cursor object
    try:
        if query_data:
            stat = self._cursor.execute(query, query_data)
        else:
            stat = self._cursor.execute(query)
    except MySQL.Error as err:
        print(err); print(query)
        return
    #END TRY/EXCEPT

    #If the query run is UPDATE or DELETE, then we return true, as the
    # code could have only gotten here by completing the query in the block above
    booleanReturn = ["update", "delete"]
    for opt in booleanReturn:
        if opt in query.lower():
            return True
        #END IF
    #END FOR
    #If the query was an insert, then we will return the row ID of the last inserted set of values
    if "insert" in query.lower():
        self._cursor.execute("SELECT LAST_INSERT_ID()")
        return self._cursor.fetchall()[0][0]
    #END IF
    #For a SELECT query, return the results
    if "select" in query.lower():
        return self._cursor.fetchall()
    #For everything else, just return the return of the execute statement
    return stat
#END DEF



# DESC: Given a SpeedTestFile object, will store it (as a pickled object) into the MySQL database.
#       The row inserted has some basic information (date time, os, etc.) and the pickled object
def storeFile(self, object, **kwargs):
    if (str(type(object)) != "<class 'source.Data_Object.SpeedTestFile.SpeedTestFile'>"):
        raise TypeError("The object passed is not a SpeedTestFile.")
    #This is a dictionary, where each key corresponds to a placeholder in the previous query.
    # Each value associated with a key will be placed into the query during execution
    query_data = {}

    for key in kwargs:
        query_data[key] = kwargs[key]


    query_data = {
        'filename': (object.Filename
                if object.Filename is not None else ''),
        'dev_id':   (object.DeviceID
                if object.DeviceID is not None else ''),
        'date':     (object.Date.split("/")[2] + "-" +
                     object.Date.split("/")[0] + "-" +
                     object.Date.split("/")[1]
                if object.Date is not None else ''),
        'time':     (object.Time
                if object.Time is not None else ''),
        'dev_type': (object.DeviceType
                if object.DeviceType is not None else ''),
        'loc_id':   (object.LocationID
                if object.LocationID is not None else ''),
        'os':       (object.OSName +", "+ object.OSArchitecture +", "+ object.OSVersion
                if object.OSName is not None else ''),
        'java':     (object.JavaVersion +", "+ object.JavaVendor
                if object.JavaVersion is not None else ''),
        'server':   (object.Server
                if object.Server is not None else ''),
        'host':     (object.Host
                if object.Host is not None else ''),
        'carrier':  (object.NetworkCarrier
                if object.NetworkCarrier is not None else ''),
        'net_prov': (object.NetworkProvider
                if object.NetworkProvider is not None else ''),
        'net_op':   (object.NetworkOperator
                if object.NetworkOperator is not None else ''),
        'con_type': (object.ConnectionType
                if object.ConnectionType is not None else ''),
        'lat':      (object.Latitude
                if object.Latitude is not None else ''),
        'long':     (object.Longitude
                if object.Longitude is not None else ''),
        'ft_year':  (object._FieldTestYear
                if object._FieldTestYear is not None else ''),
        'ft_iter':  (object._FieldTestIteration
                if object._FieldTestIteration is not None else ''),
        'bin_dat':  pickle.dumps(object, protocol=pickle.HIGHEST_PROTOCOL)
    }
    #This is a query that tests to make sure that a row does not have this duplicate information.
    # After trying to select a row with all of the information below, we fetch the results. If
    # we retrieve an ID, then we return, as we do not want to insert the file again
    query_select = ("SELECT `ID` FROM CPUC_Data.`File` \
                    WHERE `Binary_Data`=%(bin_dat)s")
    #Executing the SELECT query with the data
    fetched_data = self._executeQuery(query_select, query_data)
    if fetched_data:
        return fetched_data[0][0]
    #Now that we know that a duplicate is not present, we can run the rest of the function, inserting
    # the object's values, and the sub-objects stored in "mySpeedTests"
    #
    #Initializing the query that will be used to insert the parsed data from the raw file.
    # The information is the header information in the beginning few line of each raw data file

    # This is temporarily commented out because I am getting pickling errors
    query_insert = "INSERT INTO "+table
    for key in kwargs:
        query_insert += "'"+key+"',"
    query_insert = ("INSERT INTO CPUC_Data.`File` (`Filename`,`Device_ID`,`Date`, \
                    `Time`,`Device_Type`,`Location_ID`, \
                    `OS`,`Java`,`Server`, \
                    `Host`,`Carrier`,`Network_Provider`, \
                    `Network_Operator`,`Connection_Type`,`Latitude`, \
                    `Longitude`,`FieldTest_Year`,`FieldTest_Iteration`,`Binary_Data`)  \
                    VALUES (%(filename)s,%(dev_id)s,%(date)s, \
                    %(time)s,%(dev_type)s,%(loc_id)s, \
                    %(os)s,%(java)s,%(server)s, \
                    %(host)s,%(carrier)s,%(net_prov)s, \
                    %(net_op)s,%(con_type)s,%(lat)s, \
                    %(long)s,%(ft_year)s,%(ft_iter)s,%(bin_dat)s)")
    #Executing the INSERT query with the data. After the query has executed in the function
    # _executreQuery(), the ID of the last inserted row will be returned, and so we return that.
    return self._executeQuery(query_insert, query_data)
#END DEF



# DESC: Will return a file that met the given criteria. To call this function properly, please see the
#       documentation at the top of this file
def recallFile(self, type=(), **kwargs):
    #If the user wishes to recall a file based on the ID number (table primary key),
    # they must specify the 'type' to be "ID", and 'ID' to be the number of the row
    # they wish to retrieve
    query = ("SELECT `Binary_Data` FROM CPUC_Data.`File` \
               WHERE ")
    query_data = {}
    if "ID" in type:
        try: idNum = kwargs["ID"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the ID of the row passed through the keyword 'ID'")
        #If the program hasn't quit, then the correct options have been given
        query += "AND `ID`=%(id)s "
        query_data['id'] = idNum
    if "Device_ID" in type:
        try: dev_id = kwargs["Device_ID"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the Device ID passed through the keyword 'Device_ID'")
        query += "AND `Device_ID`=%(dev_id)s "
        query_data['dev_id'] = dev_id
    if "Date" in type:
        try: date = kwargs["Date"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the Date passed through the keyword 'Date'")
        query += "AND `Date`=%(date)s "
        query_data['date'] = date
    if "Time" in type:
        try: time = kwargs["Time"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the Time passed through the keyword 'Time'")
        query += "AND `Time`=%(time)s "
        query_data['time'] = time
    if "Location_ID" in type:
        try: loc_id = kwargs["Location_ID"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the Location_ID passed through the keyword 'Location_ID'")
        query += "AND `Location_ID`=%(loc_id)s "
        query_data['loc_id'] = loc_id
    if "Carrier" in type:
        try: carrier = kwargs["Carrier"]
        except:
            raise ValueError("This option of recall requires that you specify"+
                             " the Carrier passed through the keyword 'Carrier'")
        query += "AND `Carrier`=%(carrier)s "
        query_data['carrier'] = carrier
    #END ALL IFs

    #Just making a print out of all of the user specified options that were
    # not used by this function.
    allOpts = ["ID","Device_ID","Location_ID","Date",
               "Time","Carrier"]
    if not all([(opt in allOpts) for opt in type]):
        print("These options were not used: " +
               str([opt for opt in type if opt not in allOpts]))
    #END IF

    #Executing the query with the data. After the query has executed in the function
    # _executreQuery(), the data is returned. We then return the first element
    # of the first row returned
    fetched_data = executeQuery(query, query_data)
    #The 'if not' is checking if fetched_data is empty. If so, returns None
    if not fetched_data: return None
    return fetched_data[0][0]
#END DEF
