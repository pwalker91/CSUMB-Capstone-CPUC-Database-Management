"""
------------------------------------------------------------------------
FIELDTEST_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable

VARIABLES:
  INHERITED
    FilePath        String, holds the full path to the text file being parsed
    Filename        String, holding file name that is being parsed
    Date            String, holding the date the test was taken
    Time            String, holding the time test was taken
    EastWestSrvr    Tuple of two Strings, first String is the IP address of the East server, second the West
    Tests           Dictionary, holds all of the tests (TCP, UDP, PING, or TCRT) that have been parsed
    TestsByNum      Dictionary, holds all of the tests organized by test number
  NOT INHERITED
    OSName              String, holding OS name that this test was conducted with
    OSArchitecture      String, holding OS architecture that this test was conducted with
    OSVersion           String, holding OS version that this test was conducted with
    JavaVersion         String, holding Java version that this test was conducted with
    JavaVendor          String, holding Java vendor that this test was conducted with
    Server              String, holding Server that this test was conducted with
    Host                String, holding Host that this test was conducted with
    NetworkProvider     String, holding Network Provider that this test was conducted with (i.e. the Carrier)
    NetworkOperator     String, holding Network Operator that this test was conducted with (i.e. the Carrier)
                            note: Sometimes, the carrier name is in Network Provider, other times in Network Operator
    NetworkCarrier      String, will always hold one of the given network carriers defined in the SpeedTestDataStructure.
                            note: determined when NetworkProvider and Operator are parsed. A copy of either variable
    DeviceID            String, the Device ID number
    DeviceType          String, holding Device Type that this test was conducted with
                            note: this is either mobile or netbook
    ConnectionType      String, holding Connection type that this test was conducted with
    LocationID          Integer, the ID number of the location that this test was conducted at
    Latitude            Float, the latitude given by the GPS that this test was conducted at.
                            Is 0 if no GPS data was available
    AvgLatitude         Float, the average latitude based on all GPS measurements throughout the file
    Longitude           Float, the latitude given by the GPS that this test was conducted at.
                            Is 0 if no GPS data was available
    AvgLongitude        Float, the average longitude based on all GPS measurements throughout the file

FUNCTIONS:
  INITIALIZATION:
    __init__ - initializes the object by parsing the data in the given file path. Calls parent's __init__
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
                    filePath:   String, containing absolute path to raw data file
                    short:      Boolean, determines how this object will print out it's data when __str__ is called
        OUTPUTS-    none
    loadFieldTestInfo - initializes the object by parsing the data in the given file path.
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    findAndParseUDPTests - This takes the contents of the file being parsed, splits the content by "Staring Test"
                (to included any error messages in the tests) and the creates the UDP Test objects.
                Assumes that self._fileContentsByTest contains all of the tests
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None

  CSV VALUES
    get_csvDefaultValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the default values in a line in the CSV
    get_csvExtraValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the extra default values in a line in the CSV
    get_csvPINGValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the values parsed from the PING tests
    get_csvUDPValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the values parsed from the UDP tests
    get_csvTCPValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the values parsed from the TCP tests
    get_csvStatValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the values calculated from the values parsed from the TCP tests
    get_csvQualValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the TCP quality values calculated for each TCP test
    get_csvRvMosValues - Creates an array of values for the CSV creator
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List of Strings, the rValue and MOS scores calculated from the PING tests

  STRING PRINOUT:
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)

------------------------------------------------------------------------
"""


# IMPORTS
#Importing necessary basic_utils functions
from PyObjects.utils.basic_utils import (getFirstLineWith, monthAbbrToNum, calcTCPThroughput)
#Importing the base File class, which will take care of
# all of the basic parsing common to all files
from PyObjects._File import File
#Importing the different kinds of tests from their respective modules
from PyObjects.TCP_Test import TCP_Test
from PyObjects.UDP_Test import UDP_Test
from PyObjects.PING_Test import PING_Test
from PyObjects.TCRT_Test import TCRT_Test
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
    AvgLatitude     = 0
    Longitude       = 0
    AvgLongitude    = 0
    # ------------------------------

    # DESC: init functions calls load using the given file path
    def __init__(self, filePath=""):
        #Quick little bit of formatting
        from os.path import abspath
        filePath = abspath(filePath)
        filePath = filePath.replace("\\","")
        #Checking that the file is a Field Test file (the first line will contain "CPUC Tester")
        with open(filePath) as checkingFile:
            firstFewLines = checkingFile.read(30)
            if all( [(string not in firstFewLines) for string in ["CPUC Tester Beta","CPUC Traceroute Beta"]] ):
                raise RuntimeError("The given file is not an Iperf output file generated by a CPUC Tester.\n"+
                                    "Filename: "+filePath)
        #END WITH FILE
        #Call the parent class' __init__
        eastAndWestServerIP = ("184.72.222.65","184.72.63.139")
        File.__init__(self, filePath=filePath, eastWest=eastAndWestServerIP)
        self.loadFieldTestInfo()

        #Creating an array of the variables that we want to set to "NA" if they are empty
        emptiesToSet = ["OSName", "OSArchitecture", "OSVersion", "JavaVersion",
                        "JavaVendor", "Server", "Host", "NetworkProvider",
                        "NetworkOperator", "NetworkCarrier", "ConnectionType" ]
        self.setEmptysToDefault(attributes=emptiesToSet)

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
        #Clearing the values in self._fileContentsByTest so we don't waste some space
        self._fileContentsByTest = None
    #END INIT


# Initialization functions ---------------------------------------------------------------------

    # DESC: Parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    def loadFieldTestInfo(self):
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
            #This ELIF is for the special case when the Provider is Sprint, spelled with a lowercase
            # 's' and not a capital
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
                if getFirstLineWith(fs,"Testing started at"):
                    self.DeviceType = "Phone"
                else:
                    self.DeviceType = "Netbook"
            #END IF/ELSE

            #Get the Latitude and Longitude, if it is available
            temp = getFirstLineWith(fs, "Latitude:")
            if temp:
                self.Latitude = float(temp.split("Latitude:")[1].strip())
            temp = getFirstLineWith(fs, "Longitude:")
            if temp:
                self.Longitude = float(temp.split("Longitude:")[1].strip())

            #Reading through the contents of the file, and finding all Latitude and
            # Longitude measurements, and then averaging them (ignoring 0's)
            latitudes = []; longitudes = []
            line = "placeholder"
            while line:
                if "Latitude:" in line:
                    latitudes.append(float(line.split("Latitude:")[1].strip()))
                if "Longitude:" in line:
                    longitudes.append(float(line.split("Longitude:")[1].strip()))
                line = fs.readline()
            #END WHILE
            #Removing 0's from arrays, then calculating average of those values
            # if there are values left in the array. Otherwise, avg___ is set to 0
            latitudes = [num for num in latitudes if (num != 0)]
            self.AvgLatitude = (sum(latitudes)/len(latitudes)) if len(latitudes) else 0
            #Performing same operations as above, only now for longitudes
            longitudes = [num for num in longitudes if (num != 0)]
            self.AvgLongitude = (sum(longitudes)/len(longitudes)) if len(longitudes) else 0
        #END WITH FILE
    #END DEF

    # DESC: This takes the contents of the file being parsed, splits the content by "Staring Test"
    #       (to included any error messages in the tests) and the creates the UDP Test objects.
    #       Assumes that self._fileContentsByTest contains all of the tests
    def findAndParseUDPTests(self):
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

    # DESC: Creates an array of values for the CSV creator
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

    # DESC: Creates an array of values for the CSV creator
    def get_csvExtraValues(self):
        #csvExtraHeaders = ["Census2010", "R5Coverage", "NormalLAT", "NormalLONG" ]
        extraVals = ["NA","NA"]
        extraVals.append( "" )#self.AvgLatitude )
        extraVals.append( "" )#self.AvgLongitude )
        return extraVals
    #END DEF

    # DESC: Creates an array of values for the CSV creator
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

    # DESC: Creates an array of values for the CSV creator
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

    # DESC: Creates an array of values for the CSV creator
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
                theseTestVals = []
                for test in tcpTests:
                    theseTestVals.extend(test.get_csvDefaultValues())
                #END FOR
                if len(tcpTests) == 1:
                    theseTestVals.extend( [self.ErrorTypes[self.ErrorCode]]*2 )
                #Now we append the values for this direction to the array that
                # we are returning
                tcpVals.extend(theseTestVals)
            else:
                tcpVals.extend( [self.ErrorTypes[self.ErrorCode]]*4 )
            #END IF/ELSE
        #END FOR
        return tcpVals
    #END DEF

    # DESC: Creates an array of values for the CSV creator
    def get_csvStatValues(self):
        tcpStatVals = []
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
                theseTestVals = []
                for test in tcpTests:
                    theseTestVals.extend(test.get_csvStatValues())
                #END FOR
                if len(tcpTests) == 1:
                    theseTestVals.extend( [self.ErrorTypes[self.ErrorCode]]*4 )
                #Finally appending the values to the array that we are returning
                tcpStatVals.extend(theseTestVals)
            else:
                tcpStatVals.extend( [self.ErrorTypes[self.ErrorCode]]*8 )
            #END IF/ELSE
        #END FOR
        return tcpStatVals
    #END DEF

    # DESC: This function calls the get_csvQualValues function in each TCP test, which
    #       returns an array of the quality values for the TCP test's Upload and Download streams.
    def get_csvQualValues(self):
        tcpQualVals = []
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
                theseTestVals = []
                #This will go through each test in tcpTests, and extend the "theseTestVals" array
                # with array returned. If there was only one test, then we extend the array again with
                # four values of "No Test"
                for test in tcpTests:
                    theseTestVals.extend( test.get_csvQualValues() )
                #END FOR
                if len(tcpTests) == 1:
                    theseTestVals.extend( [self.ErrorTypes[self.ErrorCode]]*4 )
                #Finally appending the values to the array that we are returning
                tcpQualVals.extend(theseTestVals)
            else:
                tcpQualVals.extend( [self.ErrorTypes[self.ErrorCode]]*8 )
        #END FOR
        return tcpQualVals
    #END DEF

    # DESC: Creates an array of values for the CSV creator
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


# String printout ------------------------------------------------------------------------------

    # DESC: Returns a string representation of the object
    def __str__(self):
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
                    "Avg Location: ("+ str(self.AvgLatitude) +","+ str(self.AvgLongitude) +")\n" +
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
#END CLASS
