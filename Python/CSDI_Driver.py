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
          'criteria': {
                       'date': '2015-1-23',
                       'date_operator': '>='
                       },
          'statistics': 'mean'}

#results = db.select(myDict['table']+"Results", **myDict['criteria'])
if (myDict['table'] == 'TCPResults'):
    query = """SELECT TCPResults.DownSpeed, TCPResults.Id, FileInfo.NetworkCarrier FROM TCPResults JOIN FileInfo ON TCPResults.Oid = FileInfo.Id"""
    speeds = db.select('TCPResults', "Oid", "DownSpeed", DownSpeed = "0", DownSpeed_operator=">")
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
