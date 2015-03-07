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
from PyDB_API import CSDI_MySQL as dbapi

if __name__!="__main__":
    raise SystemExit


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
          "database": "CPUC",
          "autocommit": True
          }
api = dbapi(**config)
api.connect()

print("Inserting...")
for file in parsedFiles:
    print(" Inserted {} of {}...".format(parsedFiles.index(file)+1, len(parsedFiles)), end="\r")
    avgLat = [elem[0] for elem in file.AllCoordPairs if elem[0]!=0]
    avgLng = [elem[1] for elem in file.AllCoordPairs if elem[1]!=0]
    newID = api.insert( "Overview",
                        OSName_OSArchitecture_OSVersion=("{} | {} | {}".format(file.OSName,
                                                                               file.OSArchitecture,
                                                                               file.OSVersion)),
                        JavaVersion_JavaVendor=("{} | {}".format(file.JavaVersion, file.JavaVendor)),
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
        avgs = tcpTest.get_csvDefaultValues()
        sdv_md = tcpTest.get_csvStatValues()
        qual = tcpTest.get_csvQualValues()
        allValues = [elem if isinstance(elem, (float, int)) else 0 for elem in (avgs+sdv_md+qual)]
        api.insert( "TCPResult",
                    oid=newID,
                    ConnectionLoc=tcpTest.ConnectionLoc,
                    TestNumber=tcpTest.TestNumber,
                    WindowSize=tcpTest.WindowSize,
                    Port=tcpTest.Port,
                    UpSpeed=allValues[0],
                    DownSpeed=allValues[1],
                    UpStdDev=allValues[2],
                    UpMedian=allValues[3],
                    DownStdDev=allValues[4],
                    DownMedian=allValues[5],
                    UpPeriod=allValues[6],
                    UpPct=allValues[7],
                    DownPeriod=allValues[8],
                    DownPct=allValues[9],
                    ErrorType=(tcpTest.ErrorCode if tcpTest.ContainsErrors else 0)
                    )

    for udpTest in file.Tests["UDP"]:
        statVals = [elem if isinstance(elem, (float,int)) else 0 for elem in udpTest.get_csvDefaultValues()]
        api.insert( "UDPResult",
                    oid=newID,
                    ConnectionLoc=udpTest.ConnectionLoc,
                    TestNumber=udpTest.TestNumber,
                    Port=udpTest.Port,
                    DatagramSize=udpTest.DatagramSize,
                    Jitter=statVals[0],
                    Loss=statVals[1],
                    Time=statVals[2],
                    ErrorType=(udpTest.ErrorCode if udpTest.ContainsErrors else 0)
                    )

    for pingTest in file.Tests["PING"]:
        rvMos = [elem if isinstance(elem, (float, int)) else 0 for elem in pingTest.get_csvRvMosValues()]
        api.insert( "PINGResult",
                    oid=newID,
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
