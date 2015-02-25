"""
------------------------------------------------------------------------
FIELDTEST_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable

VARIABLES:

FUNCTIONS:
  INITIALIZATION:
    __new__
    __init__
    loadFieldTestInfo
    __getAllCoordinates
    findAndParseUDPTests
  CSV VALUES
    get_csvDefaultValues
    get_csvExtraValues
    get_csvPINGValues
    get_csvUDPValues
    get_csvTCPValues
    _get_csvTCPStatisticsValues
    get_csvStatValues
    get_csvQualValues
    get_csvRvMosValues
    get_csvNBNCBCValues
  STRING PRINOUT:
    __str__
------------------------------------------------------------------------
"""


# IMPORTS
import sys
import os
from platform import system
if system()=="Windows":
    import ntpath as path
else:
    import os.path as path
sys.path.append(path.dirname(__file__))

#Importing necessary basic_utils functions
from utils.basic_utils import (getLinesWith, monthAbbrToNum, calcTCPThroughput)
#Importing the base File class, which will take care of
# all of the basic parsing common to all files
from _File import File
#Importing the different kinds of tests from their respective modules
from TCP_Test import TCP_Test
from UDP_Test import UDP_Test
from PING_Test import PING_Test
from TCRT_Test import TCRT_Test
#END IMPORTS

# CLASS
class FieldTest_File(File):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # FilePath    = ""
    # Filename    = ""
    # Date        = ""
    # Time        = ""
    # EastWestSrvr = (East IP, West IP)
    # Tests       = {TCP, UDP, PING, TCRT}
    # TestsByNum  = {}
    # _fileContentsByTest = None

    # Class attributes
    OSName          = ""
    OSArchitecture  = ""
    OSVersion       = ""
    JavaVersion     = ""
    JavaVendor      = ""

    Server          = ""
    Host            = ""
    NetworkProvider = ""
    NetworkOperator = ""
    NetworkCarrier  = ""
    DeviceID        = ""
    DeviceType      = ""
    ConnectionType  = ""

    LocationID      = ""
    Latitude        = 0
    Longitude       = 0
    AllCoordPairs   = 0
    # ------------------------------


    def __new__(cls, *args, **kwargs):
        """
        Before creating an instance of the given file as a parsed object, we want to check
        that the file is indeed a test file. This will see if the necessary text
        is in the first few lines. If not, then we return None, and the object is not created
        """
        #Getting the file path that was passed in to the constructor
        if "filePath" in kwargs:
            fileLoc = kwargs["filePath"]
        else:
            fileLoc = args[0]
        #Removing any backslashes that may have been included in the file path by
        # converting the string into a representation of it (which will escape the
        # backslashes), removing the backslashes, and then the single quotes. We
        # then save the result back into fileLoc
        if system()!="Windows":
            fileLoc = path.abspath(fileLoc).replace("\\","").strip()
        #Checking that the file is indeed a FieldTest File. If not, return None
        try:
            with open(fileLoc) as checkingFile:
                firstFewLines = checkingFile.read(30)
                if all( [(string not in firstFewLines) for string in ["CPUC Tester Beta","CPUC Traceroute Beta"]] ):
                    print(fileLoc+" is not a Field Test output file")
                    return None
            #END WITH FILE
        except:
            print(fileLoc+" is a file that could not be read.")
            return None
        inst = object.__new__(cls)
        return inst
    #END DEF

    def __init__(self, filePath=""):
        """
        Initializes the object by parsing the data in the given file path. Calls parent's __init__
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            filePath:   String, containing absolute path to raw data file
        """
        #Quick little bit of formatting
        if system()!="Windows":
            filePath = path.abspath(filePath).replace("\\","").strip()

        #Call the parent class' __init__
        eastAndWestServerIP = ("184.72.222.65","184.72.63.139")
        File.__init__(self, filePath=filePath, eastWest=eastAndWestServerIP)
        self.loadFieldTestInfo()

        #Actually parsing the tests in the file
        self.findAndParseTCPTests()
        self.findAndParsePINGTests()
        self.findAndParseUDPTests()
        self.findAndParseTCRTTests()
        #This is one final check, to make sure that we have all 14 tests. If not, then
        # there was an unknown test of some kind, and we set our _contains_Errors to True
        #The 14 Tests are:
        #   2 PING TESTS (1 East, 1 West)
        #   4 TCP TESTS (2 East, 2 West)
        #   6 UDP 1 second TESTS (3 East, 3 West)
        #   2 UDP 5 second TESTS (1 East, 1 West)
        if (len(self.TestsByNum) != 14) and not self.ContainsErrors:
            self.ContainsErrors = True
            self.ErrorCode = 404
            self.ErrorMessages[404] = ("There was an unknown error of some kind, and the 14 necessary" +
                                       " tests were not performed. There are "+str(14-len(self.TestsByNum))+
                                       " tests missing.")
        #END IF
    #END INIT


# Initialization functions ---------------------------------------------------------------------

    def loadFieldTestInfo(self):
        """Parses data and info in given file (location is filePath) and stores it in the object's attributes"""
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath,'r') as fs:
            #Read in Operating System Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter="OS: ", attribute="", hasParts=True,
                                        subDelims=["Name =", "Architecture =", "Version ="],
                                        subAttrs=["OSName", "OSArchitecture", "OSVersion"] )
            #Read in Java Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter="Java: ", attribute="", hasParts=True,
                                        subDelims=["Version =", "Vendor ="],
                                        subAttrs=["JavaVersion", "JavaVendor"] )
            #Looping through pairs of delimiter and attribute pairs
            for pair in [("Server: ","Server"),("Host: ","Host"),("NetworkProvider: ","NetworkProvider"),
                         ("Network Provider: ","NetworkProvider"), ("NetworkOperator: ","NetworkOperator"),
                         ("Device ID: ","DeviceID"),("Host name: ","DeviceID"),
                         ("ConnectionType: ","ConnectionType"),("Location ID: ","LocationID"),
                         ("Location: ","LocationID")]:
                self.parseLineAndSetAttr(fileStream=fs, delimiter=pair[0], attribute=pair[1])
            #END FOR

            #Defining self.NetworkCarrier, based on the data in NetworkProvider and NetworkOperator
            if self.NetworkProvider in self.ConfirmedCarriers:
                self.NetworkCarrier = self.NetworkProvider
            elif self.NetworkOperator in self.ConfirmedCarriers:
                self.NetworkCarrier = self.NetworkOperator
            #These ELIFs are for the special cases when the Provider is 'sprint' or 'Verizon Wireless'
            elif self.NetworkProvider == "sprint":
                self.NetworkCarrier = "Sprint"
            elif self.NetworkOperator == "Verizon Wireless":
                self.NetworkCarrier = "Verizon"
            else:
                self.NetworkCarrier = "NA"
            #END IF/ELIF/ELSE

            #This is for the rare case when the Device ID was not recorded in the test for some reason
            if not self.DeviceID:
                self.DeviceID = "NA"
            #Determining Device Type, now that we know the Device ID
            if self.DeviceID != "NA":
                if "WBBDTest" in self.DeviceID:
                    self.DeviceType = "Netbook"
                else:
                    self.DeviceType = "Phone"
            else:
                if getLinesWith(fs,"Testing started at"):
                    self.DeviceType = "Phone"
                else:
                    self.DeviceType = "Netbook"
            #END IF/ELSE

            #Getting all of the Latitude and Longitude pairs from the file, and
            # then searching through them for the most accurate (ie. first pair,
            # starting from the end, to have non-zero values)
            self.AllCoordPairs = self.__getAllCoordinates(fileStream=fs)
            for pair in reversed(self.AllCoordPairs):
                if all([elem!=0 for elem in pair]):
                    self.Latitude = pair[0]
                    self.Longitude = pair[1]
                    break
            #END FOR
        #END WITH FILE

        #Creating an array of the variables that we want to set to "NA" if they are empty
        emptiesToSet = ["OSName", "OSArchitecture", "OSVersion", "JavaVersion",
                        "JavaVendor", "Server", "Host", "NetworkProvider",
                        "NetworkOperator", "NetworkCarrier", "ConnectionType" ]
        self.setEmptysToDefault(attributes=emptiesToSet)
    #END DEF

    def __getAllCoordinates(self, fileStream):
        """
        A function used by loadFieldTestInfo to parse all of the Location pairs
         (i.e. Latitude and Longitude), and save in self.AllCoordPairs
        """
        #Getting all lines with the Latitude info
        latitudes = getLinesWith(fileStream, "Latitude:")
        #Now that we have all of the latitudes, we need to go back to those locations
        # in the file and get the following lines, which contain the Longitudes
        longitudes = []
        oldLoc = fileStream.tell()
        for goodLat in latitudes:
            line = "__"
            while line:
                if goodLat in line:
                    line = fileStream.readline()
                    longitudes.append(line)
                    break
                line = fileStream.readline()
            #END WHILE
            if latitudes.index(goodLat) != (len(longitudes)-1):
                longitudes.append("Longitude: 0.0")
        #END FOR

        pairs = []
        #Now we are going to go through our three arrays, grabbing each value
        # and making a 2-element array out of the latitude and longitude.
        #We will only go along the array up to the shortest array so that we don't try to
        # index beyond the array
        for i in range( len(latitudes) ):
            pairs.append( [latitudes[i].split("Latitude:")[1].strip(),
                           longitudes[i].split("Longitude:")[1].strip()] )
        #END FOR
        #Going through each 'pair' (of three elements) and casting them to a float if they
        # are numeric. Otherwise, we assume that they are 0
        for pair in pairs:
            newPair = []
            for elem in pair:
                try:
                    elem = float(elem)
                    newPair.append(elem)
                except:
                    newPair.append(0)
            #END FOR
            pairs[pairs.index(pair)] = newPair
        #END FOR
        #Making all of our 3-element pairs into tuples
        pairs = [tuple(pair) for pair in pairs]
        return pairs
    #END DEF

    def findAndParseUDPTests(self):
        """
        This takes the contents of the file being parsed, splits the content by "Staring Test"
        (to included any error messages in the tests) and the creates the UDP Test objects.
        Assumes that self._fileContentsByTest contains all of the tests
        """
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                if "UDP" in chunk:
                    if "1 second Test" in chunk:
                        try:
                            #This block gets the test number from the beginning of this chunk of
                            # characters. Each 1 second test has a different test number, as 3 are
                            # run in sequence. The number stored in tempTestNum applies to all 3
                            allStartingLine = ""
                            tempTestNum = 0
                            for line in chunk.split("\n"):
                                if ("Starting Test" in line) and (tempTestNum == 0):
                                    allStartingLine = line+"\n"
                                    rightChunk = line.split("Starting Test ")[1].strip()
                                    tempTestNum = rightChunk.split(":")[0].split("..")[0]
                                    break
                            #END FOR
                            subTests = chunk.split("Starting UDP 1")[1:]
                            subTests = [(allStartingLine+"Starting UDP 1"+text) for text in subTests]
                            #Now we go through each 1 second test, parse it into a UDP_Test object,
                            # and appended it to the array parsedSubTests. This array will then be
                            # added to self.Tests in the UDP and NUM category
                            for test in subTests:
                                #The if statement is one last check to make sure that the test actually contains
                                # some basic information
                                if "Iperf command line" in test:
                                    parsedTest = UDP_Test(dataString=test, eastWest=self.EastWestSrvr)
                                    tempSubTestNum = test.split("Test #")[1].split("\n")[0].strip()
                                    parsedTest.TestNumber = int(tempTestNum)
                                    parsedTest.SubTestNumber = int(tempSubTestNum)
                                    self.Tests[parsedTest.ConnectionType].append(parsedTest)
                                    #Determining the index for this "sub" test
                                    byNum = float(str(parsedTest.TestNumber)+"."+str(parsedTest.SubTestNumber))
                                    self.TestsByNum[byNum] = parsedTest
                                #END IF
                            #END FOR
                        except:
                            raise RuntimeError("Something went wrong when trying to put the UDP test into this "+
                                               "File object.\nFilePath: "+self.FilePath)
                        #END TRY/EXCEPT
                    else:
                        try:
                            #The chunk holds a 5 second UDP Test, so we pass it to the constructor, and then
                            # append the test to our tests. We append in two places; in the UDP category
                            # and in the NUM category (inserted at the index that corresponds to the test number)
                            #The if statement is one last check to make sure that the test actually contains
                            # some basic information
                            if "Iperf command line" in chunk:
                                parsedTest = UDP_Test(dataString=chunk, eastWest=self.EastWestSrvr)
                                self.Tests[parsedTest.ConnectionType].append(parsedTest)
                                self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                            #END IF
                        except:
                            raise RuntimeError("Something went wrong when trying to put the UDP test into this "+
                                               "File object.\nFilePath: "+self.FilePath)
                        #END TRY/EXCEPT
                    #END IF/ELSE
                #END IF
            #END FOR
        #END IF
    #END DEF


# Creating values for CSV ----------------------------------------------------------------------

    def get_csvDefaultValues(self, **kwargs):
        if 'device_tester_table' not in kwargs.keys():
            raise KeyError("The keyword argument 'device_tester_table' must be defined.")
        if not isinstance(kwargs['device_tester_table'], str):
            raise ValueError("The 'device_tester_table' must be a single string.")
        defaultVals = []
        #Calculating the Tester number
        testerVal = "NA"
        dt_table = kwargs['device_tester_table']
        if dt_table and self.DeviceID in dt_table:
            dt_table = dt_table.split("\n")
            for line in dt_table:
                if self.DeviceID in line:
                    testerVal = line.split(",")[1].strip()
            #END FOR
        #END IF
        defaultVals.append( testerVal )
        defaultVals.append( self.LocationID )
        defaultVals.append( self.Date )
        defaultVals.append( self.Time )
        defaultVals.append( self.NetworkProvider )
        defaultVals.append( self.NetworkOperator )
        defaultVals.append( self.ConnectionType )
        defaultVals.append( self.Latitude )
        defaultVals.append( self.Longitude )
        defaultVals.append( self.DeviceID )
        defaultVals.append( self.DeviceType )
        return defaultVals
    #END DEF

    def get_csvExtraValues(self):
        #csvExtraHeaders = ["Census2010", "R5Coverage", "NormalLAT", "NormalLONG" ]
        extraVals = ["NA","NA"]
        extraVals.append( "" )#self.AvgLatitude )
        extraVals.append( "" )#self.AvgLongitude )
        return extraVals
    #END DEF

    def get_csvPINGValues(self):
        #This arrat will hold all of the Ping values that will be in the csv
        pingVals = []
        #Get the RTT Min, Max, Average, and calculate the percent loss of packets in the PING test
        for connLoc in ["West", "East"]:
            pingTest = self.getTest("PING", ConnectionLoc=connLoc)
            try:
                pingVals.extend(pingTest[0].get_csvDefaultValues())
            except:
                pingVals.extend([self.ErrorTypes[self.ErrorCode]]*4)
        #END FOR
        return pingVals
    #END DEF

    def get_csvUDPValues(self):
        udpVals = []
        #We are going loop through all of the sub test numbers in order, and with each sub test number,
        # we get the East test, and then the West test, getting the default CSV values from each test
        for connLoc in ["West", "East"]:
            for subTestNum in [1, 2, 3]:
                udpTest = self.getTest("UDP", TestInterval=1,
                                        SubTestNumber=subTestNum, ConnectionLoc=connLoc)
                try:
                    udpVals.extend(udpTest[0].get_csvDefaultValues())
                except:
                    udpVals.extend([self.ErrorTypes[self.ErrorCode]]*3)
            #END FOR
            #Now we get the 5 second interval East test, and get it's default CSV values, which are
            # appended to the array that we will return
            udpTest = self.getTest("UDP", TestInterval=5, ConnectionLoc=connLoc)
            try:
                udpVals.extend(udpTest[0].get_csvDefaultValues())
            except:
                udpVals.extend([self.ErrorTypes[self.ErrorCode]]*3)
        #END FOR
        #Now that we have our array, we return it
        return udpVals
    #END DEF

    def get_csvTCPValues(self):
        tcpVals = []
        #Getting the values need for the TCP tests. If a test does not exist, then
        # it's placeholder is "No Test"
        for connLoc in ["West", "East"]:
            tcpTests = self.getTest("TCP", ConnectionLoc=connLoc)
            #If there are tests, then we calculate the necessary values
            if tcpTests:
                #This is just a quick test to see if the TCP tests are in order by number.
                # If they aren't then we swap them
                if (len(tcpTests) == 2) and (tcpTests[0].TestNumber > tcpTests[1].TestNumber):
                    #This is a quick swap
                    tcpTests[0], tcpTests[1] = tcpTests[1], tcpTests[0]
                #END IF
                _partial_tcpVals = []
                for test in tcpTests:
                    _partial_tcpVals.extend(test.get_csvDefaultValues())
                #END FOR
                if len(tcpTests) == 1:
                    _partial_tcpVals.extend( [self.ErrorTypes[self.ErrorCode]]*2 )
                #Now we append the values for this direction to the array that
                # we are returning
                tcpVals.extend(_partial_tcpVals)
            else:
                tcpVals.extend( [self.ErrorTypes[self.ErrorCode]]*4 )
            #END IF/ELSE
        #END FOR
        return tcpVals
    #END DEF

    def _get_csvTCPStatisticsValues(self, typ, count):
        """
        This takes a type of statistics that we wish to get from a TCP Test, and
        calls the necesssary function from our TCP tests.
        ARGS:
            typ     String, the type of statistics we want [Stat, Qual, ...]
            count   Integer, the expected number of values returned
        """
        if typ not in ["Stat","Qual"]:
            raise ValueError("We cannot perform a statistics function of the type you requested.\n"+
                            "The type must be one of the following: "+str(["Stat","Qual"]))
        #END IF
        tcpVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tcpTests = self.getTest("TCP", ConnectionLoc=connLoc)
            #If there are tests, then we calculate the necessary values
            if tcpTests:
                #This is just a quick test to see if the TCP tests are in order by number.
                # If they aren't then we swap them
                if (len(tcpTests) == 2) and (tcpTests[0].TestNumber > tcpTests[1].TestNumber):
                    #This is a quick swap
                    tcpTests[0], tcpTests[1] = tcpTests[1], tcpTests[0]
                #END IF
                _partial_tcpVals = []
                for test in tcpTests:
                    getStatistics = getattr(test, "get_csv"+typ+"Values")
                    _partial_tcpVals.extend(getStatistics())
                #END FOR
                if len(tcpTests) == 1:
                    _partial_tcpVals.extend( [self.ErrorTypes[self.ErrorCode]]*count )
                #Finally appending the values to the array that we are returning
                tcpVals.extend(_partial_tcpVals)
            else:
                tcpVals.extend( [self.ErrorTypes[self.ErrorCode]]*(count*2) )
            #END IF/ELSE
        #END FOR
        return tcpVals
    #END DEF

    def get_csvStatValues(self):
        return self._get_csvTCPStatisticsValues("Stat", 4)
    #END DEF

    def get_csvQualValues(self):
        return self._get_csvTCPStatisticsValues("Qual", 4)
    #END DEF

    def get_csvRvMosValues(self):
        rValMOSVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            pingTests = self.getTest("PING", ConnectionLoc=connLoc)
            if pingTests:
                rValMOSVals.extend( pingTests[0].get_csvRvMosValues() )
            else:
                rValMOSVals.extend( [self.ErrorTypes[self.ErrorCode]]*2 )
        #END FOR
        return rValMOSVals
    #END DEF

    def get_csvNBNCBCValues(self):
        """
        This will conglomerate all upload speed from every TCP test into one
        list. The same will also be done with the download speeds.
        Once our lists have all 4 TCP test's speeds, we will then take the mean,
        the population standard deviation, and then calculate the mean minus
        one standard deviation.
        RETURNS:
            NBNValues   List of 6 values, the mean, population standard deviation,
                        and (mean-pstdev) of a combination of all thread from every
                        test in each direction.
        """
        from statistics import mean, pstdev
        allTCPs = self.getTest("TCP")
        upMsrments = []; dnMsrments = []
        #We will only perform these functions and math if allTCPs actually
        # returned tests for us to use
        if allTCPs:
            for test in allTCPs:
                if not test.ContainsErrors:
                    upMsrments.append(mean(test.get_ThreadSumValues(direction="UP")))
                    dnMsrments.append(mean(test.get_ThreadSumValues(direction="DOWN")))
            #END FOR
            if upMsrments:
                upMean = mean(upMsrments); upStDev = pstdev(upMsrments)
            else:
                upMean = -1; upStDev = -1;
            #END IF/ELSE
            if dnMsrments:
                dnMean = mean(dnMsrments); dnStDev = pstdev(dnMsrments)
            else:
                dnMean = -1; dnStDev = -1;
            #END IF/ELSE
            NBNVals = [upMean, upStDev, (upMean-upStDev),
                       dnMean, dnStDev, (dnMean-dnStDev)]
        else:
            NBNVals = [self.ErrorTypes[self.ErrorCode]]*6
        return NBNVals
    #END DEF


# String printout ------------------------------------------------------------------------------

    # DESC: Returns a string representation of the object
    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding +
                    "Filename: " + str(self.Filename) + "\n" +
                self.StringPadding +
                    "Location ID: " + str(self.LocationID) + "\n" +
                self.StringPadding +
                    "DateTime of Speed Test: " + str(self.Date) +" "+ str(self.Time) + "\n" +
                self.StringPadding +
                    "Device ID: " + str(self.DeviceID) + "\n" +
                self.StringPadding +
                    "Device Type: " + str(self.DeviceType) + "\n" +
                self.StringPadding +
                    "Network Carrier: " + str(self.NetworkCarrier) + "\n" +
                self.StringPadding +
                    "Network: Provider = " + str(self.NetworkProvider) +
                    ", Operator = " + str(self.NetworkOperator) + "\n" +
                self.StringPadding +
                    "Connection Type: " + str(self.ConnectionType) + "\n" +
                self.StringPadding +
                    "OS: " + str(self.OSName) +", "+ str(self.OSArchitecture) +", "
                    + str(self.OSVersion) + "\n" +
                self.StringPadding +
                    "Java: " + str(self.JavaVersion) +", "+ str(self.JavaVendor) + "\n" +
                self.StringPadding +
                    "Connection: Server = " + str(self.Server) +", Host = " + str(self.Host) + "\n" +
                self.StringPadding +
                    "Location: ("+ str(self.Latitude) +","+ str(self.Longitude) +")\n" +
                self.StringPadding +
                    "Contain Major Errors: " + repr(self.ContainsErrors) + "\n" +
                    ((self.StringPadding + \
                        "Error Type: " + self.ErrorTypes[self.ErrorCode] + "\n") \
                      if self.ContainsErrors else "" ) +
                    ((self.StringPadding + \
                        "Error Message: " + self.ErrorMessages[self.ErrorCode] + "\n") \
                      if self.ContainsErrors else "" ) +
                self.printTests()
                )
    #END DEF

    '''
    def __repr__(self):
        """Returns a string of all of the attributes in this object"""
        string = ""
        for elem in self.__dict__:
            string += elem+":   "+str(self.__dict__[elem])+"\n"
        return string
    #END DEF
    '''
#END CLASS
