#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
RUN.PY

AUTHOR:     Peter Walker (pwalker@csumb.edu)

PURPOSE:    This takes a hard-coded folder of values, parses them with the
              FileParser module, and then stored them in a local MySQL database
              with the PyDB_API module.
            The MySQL connection information is hard coded into the DB API
--------------------------------------------------------------------------------
"""

import os
import sys
import statistics
import datetime

from FileParser.FieldTest_File import FieldTest_File as parser
from CSDI_MySQL import CSDI_MySQL as dbapi

if __name__!="__main__":
    raise SystemExit


def _getTCPVals(tcpTest):
    """Returns a List of the default CSV values needed for the creation of a CSV"""
    csvVals = []
    #If there was no error, there are values to calculate
    # Otherwise, we return an array of "self._error_Type"
    if not tcpTest.ContainsErrors:
        upSum = 0
        dnSum = 0
        for thread in tcpTest.Threads["UP"]:
            upSum += thread.FinalMsmt.Speed
        for thread in tcpTest.Threads["DOWN"]:
            dnSum += thread.FinalMsmt.Speed
        csvVals = [upSum, dnSum]
    else:
        csvVals = [tcpTest.ErrorType]*2
    return csvVals
#END DEF

def _getTCPStatValues(tcpTest):
    """
    This creates an array of 4 values that will be appended to the Results CSV
     provided by CPUC. If there was an error in the test, the 4 values returned are the error type.
     Otherwise, the 4 values are the StDev and Median for both thread directions for this test
    """
    csvVals = []
    #If there was no error, there are values to StDev and Median
    # Otherwise, we return an array of "None"
    if not tcpTest.ContainsErrors:
        #Calculating the stDev's and medians of the Up and Down threads
        upThread = tcpTest.get_ThreadSumValues(direction="UP", attribute="Speed")
        downThread = tcpTest.get_ThreadSumValues(direction="DOWN", attribute="Speed")
        csvVals.append( statistics.pstdev(upThread) )
        csvVals.append( statistics.median(upThread) )
        csvVals.append( statistics.pstdev(downThread) )
        csvVals.append( statistics.median(downThread) )
    else:
        csvVals = [tcpTest.ErrorType]*4
    return csvVals
#END DEF

def _TCPPeriod(tcpTest):
    if not tcpTest.ContainsErrors:
        PERIOD = {"UP": [], "DOWN": [] }
        for direction in PERIOD:
            #This block calculates the TCP Quality based on the total time
            # it took the thread to complete their downloads
            #For each thread, get the total time (final measurement timeEnd)
            for thread in tcpTest.Threads[direction]:
                PERIOD[direction].append(thread.FinalMsmt.TimeEnd)
            #END FOR
        #This creates an array of average upload times (the average PERIOD)
        qualVals = [statistics.mean(PERIOD["UP"]),statistics. mean(PERIOD["DOWN"])]
    else:
        qualVals = [tcpTest.ErrorType]*2
    return qualVals
#END DEF

def _TCPRating(tcpTest):
    if not tcpTest.ContainsErrors:
        RATING = {"UP": [], "DOWN": []}
        for direction in RATING:
            #This block calculates the TCP Quality based on the data score,
            # a value between 1 and 0 based on how many intervals in the threads were
            # either downloading or uploading data
            allSpeeds = tcpTest.get_ThreadsValues(direction=direction)
            for thread in allSpeeds:
                for elem in thread:
                    if elem>0:
                        RATING[direction].append(1)
                    else:
                        RATING[direction].append(0)
            #END FOR
        #END FOR
        qualVals = [statistics.mean(RATING["UP"]), statistics.mean(RATING["DOWN"])]
    else:
        qualVals = [tcpTest.ErrorType]*2
    return qualVals
#END DEF





# MAIN -------------------------------------------------------------------------

FILELOCATION = "/Users/peterwalker/Desktop/toparse/rawdata/"

parsedFiles = []

print("Parsing...")
for file in os.listdir(FILELOCATION):
    truePath = os.path.join(FILELOCATION, file)
    parsed = parser(truePath)
    if parsed:
        parsedFiles.append(parsed)


print("Connecting...")
config = {"user": "root",
          "host": "localhost",
          "password": "thedefault",
          "database": "Capstone",
          "autocommit": True
          }
db = dbapi(**config)
db.connect()

print("Inserting...")
for file in parsedFiles:
    print(" Inserted {} of {} records...".format(parsedFiles.index(file)+1, len(parsedFiles)), end="\r")
    avgLat = [elem[0] for elem in file.AllCoordPairs if elem[0]!=0]
    avgLng = [elem[1] for elem in file.AllCoordPairs if elem[1]!=0]
    newID = db.insert( "FileInfo",
                        OSName=file.OSName,
                        OSArchitecture=file.OSArchitecture,
                        OSVersion=file.OSVersion,
                        JavaVersion=file.JavaVersion,
                        JavaVendor=file.JavaVendor,
                        DeviceID=file.DeviceID,
                        DeviceType=file.DeviceType,
                        Server=file.Server,
                        Host=file.Host,
                        NetworkCarrier=file.NetworkCarrier,
                        NetworkProvider=file.NetworkProvider,
                        NetworkOperator=file.NetworkOperator,
                        ConnectionType=file.ConnectionType,
                        LocationID=file.LocationID,
                        Date=datetime.datetime.strptime(file.Date,"%m/%d/%Y").strftime("%Y-%m-%d"),
                        Time=file.Time,
                        Latitude=file.Latitude,
                        AvgLatitude=(statistics.mean(avgLat) if len(avgLat)>0 else 0),
                        Longitude=file.Longitude,
                        AvgLongitude=(statistics.mean(avgLng) if len(avgLng)>0 else 0),
                        ErrorType=(file.ErrorCode if file.ContainsErrors else 0)
                        )

    for tcpTest in file.Tests["TCP"]:
        avgs = _getTCPVals(tcpTest)
        sdv_md = _getTCPStatValues(tcpTest)
        qual = _TCPPeriod(tcpTest)+_TCPRating(tcpTest)
        allValues = [elem if isinstance(elem, (float, int)) else 0 for elem in (avgs+sdv_md+qual)]
        db.insert( "TCPResults",
                    Oid=newID,
                    ConnectionLoc=tcpTest.ConnectionLoc,
                    TestNumber=tcpTest.TestNumber,
                    WindowSize=(tcpTest.WindowSize if not tcpTest.ContainsErrors else 0),
                    Port=(tcpTest.Port if not tcpTest.ContainsErrors else 0),
                    UpSpeed=allValues[0],
                    DownSpeed=allValues[1],
                    UpStdDev=allValues[2],
                    UpMedian=allValues[3],
                    DownStdDev=allValues[4],
                    DownMedian=allValues[5],
                    UpPeriod=allValues[6],
                    DownPeriod=allValues[7],
                    UpPct=allValues[8],
                    DownPct=allValues[9],
                    ErrorType=(tcpTest.ErrorCode if tcpTest.ContainsErrors else 0)
                    )

    for udpTest in file.Tests["UDP"]:
        statVals = []
        if not udpTest.ContainsErrors:
            statVals.append(udpTest.Threads[0].ServerReport.Jitter)
            statVals.append(udpTest.Threads[0].ServerReport.Dtgrams_Perc)
            statVals.append(udpTest.TestInterval)
        else:
            statVals = [0]*3
        db.insert( "UDPResults",
                    Oid=newID,
                    ConnectionLoc=udpTest.ConnectionLoc,
                    TestNumber=udpTest.TestNumber,
                    Port=(udpTest.Port if not tcpTest.ContainsErrors else 0),
                    DatagramSize=(udpTest.DatagramSize if not tcpTest.ContainsErrors else 0),
                    Jitter=statVals[0],
                    Loss=statVals[1],
                    Time=statVals[2],
                    ErrorType=(udpTest.ErrorCode if udpTest.ContainsErrors else 0)
                    )

    for pingTest in file.Tests["PING"]:
        rvMos = [elem
                 if isinstance(elem, (float, int)) else 0
                 for elem in pingTest.calc_rValMOS()]
        db.insert( "PINGResults",
                    Oid=newID,
                    ConnectionLoc=pingTest.ConnectionLoc,
                    TestNumber=pingTest.TestNumber,
                    PacketsSent=pingTest.PacketsSent,
                    PacketsReceived=pingTest.PacketsReceived,
                    PacketsLost=pingTest.PacketsLost,
                    RTTMin=pingTest.RTTMin,
                    RTTMax=pingTest.RTTMax,
                    RTTAverage=pingTest.RTTAverage,
                    RValue=rvMos[0],
                    MOS=rvMos[1],
                    ErrorType=(pingTest.ErrorCode if pingTest.ContainsErrors else 0)
                    )
print()
#END MAIN
