"""README
    So to first explain how I want this to work, I was thinking something along the lines like this:
            Go through json data to find what table that is being asked to be queried
            Based on the table, go through if/else statements to do the correct select statement for speeds and dates. For right now strictly doing speeds vrs dates
            For the speeds select statement and date select statement, based on FK's assign speed and dates to their specific arrays
            Send data to MPL"""

import sys
import json
from CSDI_MySQL import CSDI_MySQL as db#talk to them
#from CSDI_matplotlib_adv.py import CSDI_MPL as mpl

myDict = {'table':'TCPResults',
          'table_val':'Throughtput',
          'file_criteria': {
                       'date': '2015-1-23',
                       'date_operator': '>='
                       },
          'test_criteria': {
            'DownSpeed':100
            'DownSpeed_comparator':"<="
          },
          'grouping': "NetworkCarrier",
          'statistics': 'mean'}

#results = db.select(myDict['table']+"Results", **myDict['criteria'])
if (myDict['table'] == 'TCPResults'):
    query = """SELECT TCPResults.DownSpeed, TCPResults.Id, FileInfo.NetworkCarrier FROM TCPResults JOIN FileInfo ON TCPResults.Oid = FileInfo.Id"""
    dates = db.select('FileInfo', "*", Date = myDict['file_criteria']['date'], Date_operator= myDict['date_operator'])
    for ID in dates:
        speeds = db.select(myDict['table'], "*", Oid=ID, DownSpeed = "0", DownSpeed_operator=">")
        for value in speeds:
            values[dates['NetworkCarrier']].append(speeds[myDict['table_val']])
    print(speeds)
#from here:
""" 1) do forloop to collect speeds for when
    Oid from "speeds" == Id from "dates"
    2) in same for loop for dates store dates in seperate array where
    Oid == Id

    Example:
    for rows in speeds:
    if (dates['Id'] == speeds['Oid'])
    store speeds
    for rows in dates:
    if (dates['Id'] == speeds['Oid'])
    store according dates
    3) send data to mpl api
    4) issues:
    When running select statement:
    "args[0].cursor.execute("SHOW COLUMNS FROM {}".format(args[1]))
    AttributeError: 'str' object has no attribute 'cursor'"
    5) Pretty sure the select statement is correct"""
if (myDict['table'] == 'UDPResults'):
    speeds = db.select('UDPResults', "Oid", "DownSpeed", DownSpeed = "0",DownSpeed_operator=">")
    dates = db.select('FileInfo', "Id", "Date", Date = myDict['date'], Date_operator= myDict['date_operator'])
    print(speeds)
    #from here:
    """ 1) do forloop to collect speeds for when
            Oid from "speeds" == Id from "dates"
        2) in same for loop for dates store dates in seperate array where
            Oid == Id
            Example:
                for rows in speeds:
                    if (dates['Id'] == speeds['Oid'])
                        store speeds
                for rows in dates:
                    if (dates['Id'] == speeds['Oid'])
                        store according dates
        3) send data to mpl api
        4) issues:
            When running select statement:
                "args[0].cursor.execute("SHOW COLUMNS FROM {}".format(args[1]))
                AttributeError: 'str' object has no attribute 'cursor'"
        5) Pretty sure the select statement is correct"""



"""
After if/else statements
send data to graph maybe like
graph(speeds, dates, myDict['statistics'])
"""





VALUES = { "AT&T": [1,45,123,5,1,4,5,54,1,243,5,12,51,23,54,123,5,123,51],
           "Verizon": [234,5,7,1,23,21,35,5678,6,346,12,12,34,12345,1,23,4,234],
           "T-Mobile": [1234,5,5123,123,51,256,123,5,1235],
           "Sprint": [1235,6,1,1,3,6,7,86,346823,46,2134,51,253,512,35]
           }

VALUES["AT&T"]
STDEVS = {}
or
for key in VALUES:
    STDEVs[key] = statistics.pstdev(VALUES[key])
    MEANS[key] = statistics.mean(VALUES[key])
















#js = results[0]['AnalysisOpts']
#js_data = json.loads(js)
"""json_data = {'table':'TCP',
            'criteria': {
                'date': 'somedate',
                'date_operator': '>='
            },
            'statistics': 'mean'}


if json_data['statistics'] == 'mean':
    do stuff
elif json_data['statistics'] == 'average':"""
