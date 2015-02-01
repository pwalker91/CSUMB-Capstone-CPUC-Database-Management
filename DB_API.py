
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
