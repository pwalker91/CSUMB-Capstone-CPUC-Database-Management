"""
------------------------------------------------------------------------
CROWDSOURCE_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable

FUNCTIONS:
  INITIALIZATION:
    __new__
    __init__
    loadCrowdSourceInfo
    __getLocationCoords
    findAndParseUDPTests
  CSV VALUES
    get_csvDefaultValues
    get_csvExtraValues
    _get_csvValues
    get_csvPINGValues
    get_csvUDPValues
    get_csvTCPValues
    get_csvStatValues
    get_csvQualValues
    get_csvRvMosValues
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

#Importing necessary data_utils functions
from utils.basic_utils import (getLinesWith, monthAbbrToNum, calcTCPThroughput)
#Importing the base File class, which will take care of
# all of the basic parsing common to all files
from _File import File
#Importing the different kinds of tests from their respective modules
from TCP_Test import TCP_Test
from UDP_Test import UDP_Test
from PING_Test import PING_Test
#END IMPORTS

# CLASS
class CrowdSource_File(File):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # FilePath    = ""
    # Filename    = ""
    # Date        = ""
    # Time        = ""
    # EastWestSrvr = (East IP, West IP)
    # Tests       = {TCP, UDP, PING, NUM}
    # TestsByNum  = {}
    # _fileContentsByTest = None

    # Class attributes
    ClientType      = ""
    AppVersion      = ""

    OSName          = ""
    OSArchitecture  = ""
    OSVersion       = ""
    JavaVersion     = ""
    JavaVendor      = ""

    Server          = ""
    Host            = ""
    NetworkProvider = ""
    NetworkOperator = ""
    NetworkType     = ""
    ConnectionType  = ""
    ConnectionName  = ""

    Roaming         = None
    Environment     = ""

    PhoneModel      = ""
    PhoneManufac    = ""
    PhoneAPIVer     = ""
    PhoneSDKVer     = ""

    WiFiBSSID       = ""
    WiFiSSID        = ""

    LocationSource  = ""
    Latitude        = 0
    Longitude       = 0
    DistanceMoved   = 0

    #For Phone AppVersion v1.0 ONLY
    AllCoordPairs = None

    #For Phone AppVersion v1.1+
    AllGPSCoordPairs = None
    GPSLastKnownCoord = None
    AllNetworkCoordPairs = None
    NetworkLastKnownCoord = None

    #If ClientType is "Desktop", these attributes are used for information
    # ClientType
    # AppVersion
    # OSName
    # OSArchitecture
    # OSVersion
    # PhoneAPIVer       (same as OSName if "Windows", OSVersion if "Mac")
    # LocationSource
    # NetworkProvider   (is really Network ISP)
    # Environment       (Type of Operating System)
    # ConnectionName    (is a List)
    # ConnectionType    (is a List)
    # Latitude
    # Longitude

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
                if all( [(string not in firstFewLines) for string in ["Crowd Source"]] ):
                    print(fileLoc+" is not a Crowd Source Test output file")
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
        eastAndWestServerIP = ("174.129.206.169","54.241.14.161")
        File.__init__(self, filePath=filePath, eastWest=eastAndWestServerIP)
        self.loadCrowdSourceInfo()

        #Actually parsing the tests in this file
        self.findAndParseTCPTests()
        self.findAndParsePINGTests()
        self.findAndParseUDPTests()
        #This is one final check, to make sure that we have all 6 tests. If not, then
        # there was an unknown test of some kind, and we set our ContainsErrors to True
        #The 6 Tests are:
        #   2 PING TESTS (1 East, 1 West)
        #   2 TCP TESTS (1 East, 1 West)
        #   2 UDP 1 second TESTS (1 East, 1 West)
        if (len(self.TestsByNum) != 6) and not self.ContainsErrors:
            self.ContainsErrors = True
            self.ErrorCode = 404
            self.ErrorMessages[404] = ("There was an unknown error of some kind, and the 14 necessary" +
                                       " tests were not performed. There are "+str(6-len(self.TestsByNum))+
                                       " tests missing.")
        #END IF
    #END INIT


# Initialization functions ---------------------------------------------------------------------

    def loadCrowdSourceInfo(self):
        """Initializes the object by parsing the data in the given file path from __init__."""
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath,'r') as fs:
            #We are going to first get the line that contains some of the basic
            # information, like the Client Type and the App Version
            temp = getLinesWith(fs,"Crowd Source")
            if temp:
                if "Phone" in temp[0]:
                    self.ClientType = "Phone"
                elif "Desktop" in temp[0]:
                    self.ClientType = "Desktop"
                else:
                    self.ClientType = "UNKNOWN"
                #END IF/ELIF/ELSE
                version = temp[0].split("v")[1].strip()
                self.AppVersion = "v"+version
            else:
                raise RuntimeError("This file is not a Crowd Source CPUC file.")
            #END IF/ELSE
            #If the device was a phone, then we will parse accordingly
            if self.ClientType == "Phone":
                #Setting the values of our class variables
                #Read in Operating System Header Information
                self.parseLineAndSetAttr(fileStream=fs, delimiter="OS: ", attribute="", hasParts=True,
                                            subDelims=["Name =", "Architecture =", "Version ="],
                                            subAttrs=["OSName", "OSArchitecture", "OSVersion"] )
                #Read in Java Header Information
                self.parseLineAndSetAttr(fileStream=fs, delimiter="Java: ", attribute="", hasParts=True,
                                            subDelims=["Version =", "Vendor ="],
                                            subAttrs=["JavaVersion", "JavaVendor"] )
                #Read in many other values
                for pair in [("Server:","Server"),("Host:","Host"),("NetworkProvider:","NetworkProvider"),
                             ("NetworkOperator:","NetworkOperator"),("NetworkType:","NetworkType"),
                             ("ConnectionType:","ConnectionType"),("This device was","Environment"),
                             ("Phone Model:","PhoneModel"),("Phone Manufacturer:","PhoneManufac"),
                             ("API Version:","PhoneAPIVer"),("SDK Version:","PhoneSDKVer"),
                             ("WiFi BSSID:","WiFiBSSID"),("WiFi SSID:","WiFiSSID")]:
                    self.parseLineAndSetAttr(fileStream=fs, delimiter=pair[0], attribute=pair[1])

                #Determining if the device was Roaming or not.
                line = getLinesWith(fs, "Network is Roaming.")
                if line: self.Roaming = True
                line = getLinesWith(fs, "Network is Not Roaming.")
                if line: self.Roaming = False
                #Sometimes, there was a ":" in the output of the environment. This
                # little block below removes that
                self.Environment = self.Environment.replace(":","").strip()

                #The Latitude and Longitude information between app versions is different, so
                # we need to have separate blocks for each. The main difference is that v1.0 has
                # just Latitude and Longitude, while v1.1 and later have GPS Lat, GPS Long,
                # Network Lat, and NetworkLong
                if self.AppVersion == "v1.0":
                    #The Location source for v1.0 was always GPS, and Distance Moved does not apply
                    self.LocationSource = "GPS"
                    self.DistanceMoved = 0
                    self.AllCoordPairs = self.__getLocationCoords(fs, "")
                    for triplet in reversed(self.AllCoordPairs):
                        if triplet[0] != 0 and triplet[1] != 0:
                            self.Latitude = triplet[0]
                            self.Longitude = triplet[1]
                    #END FOR
                #If the App Version is v1.1 or greater, then we have GPS Lat/Long and
                # Network Lat/Long. This big block will determine which is most accurate,
                # distance moved for each, and all that jazz
                else:
                    self.AllGPSCoordPairs = self.__getLocationCoords(fileStream=fs, typ="GPS")
                    self.AllNetworkCoordPairs = self.__getLocationCoords(fileStream=fs, typ="Network")
                    #Now that we have all of the coordinate pairs, we need to determine which pair
                    # is the one to record. The priority is...
                    #     GPS
                    #     Network
                    #     Last Known GPS
                    #     Last Known Network
                    #We are going to sequentially look at each triplet of coordinates
                    # from the Network and GPS. First, we loop through a reverse of all of the
                    # GPS coordinates. If we find a pair of Lat/Long that are not zero, then we user
                    # that coordinate and break.
                    for triplet in reversed(self.AllGPSCoordPairs):
                        #These two conditionals are checking that the Latitude and Longitude values
                        # are all non-zero
                        if triplet[0] != 0 and triplet[1] != 0:
                            self.Latitude = triplet[0]
                            self.Longitude = triplet[1]
                            self.DistanceMoved = triplet[2]
                            self.LocationSource = "GPS"
                            break
                    #END FOR
                    #If the previous loop did not set the Latitude and Longitude values, then
                    # we will look through the Network location measurements
                    if not self.LocationSource:
                        for triplet in reversed(self.AllNetworkCoordPairs):
                            if triplet[0] != 0 and triplet[1] != 0:
                                self.Latitude = triplet[0]
                                self.Longitude = triplet[1]
                                self.DistanceMoved = triplet[2]
                                self.LocationSource = "Network"
                                break
                        #END FOR
                    #END IF

                    #Function to parse and set the LastKnowLat/Long for both GPS and Network
                    def _getLastKnown(fileStream, pair, attr):
                        line1 = getLinesWith(fs, pair[0])[0]
                        line2 = getLinesWith(fs, pair[1])[0]
                        if "no value" not in line1.lower() and "no value" not in line2.lower():
                            self.__dict__[attr] = ( float(line1.split(pair[0])[1].strip()),
                                                        float(line2.split(pair[1])[1].strip()))
                        else:
                            self.__dict__[attr] = (0,0)
                    #Loop to call the function for GPS and Network
                    for argss in [(("GPSLastKnownLat:","GPSLastKnownLong:"), "GPSLastKnownCoord"),
                                  (("NetworkLastKnownLat:","NetworkLastKnownLong:"), "NetworkLastKnownCoord")]:
                        _getLastKnown(fs, argss[0], argss[1])
                    #END FOR

                    if not self.LocationSource:
                        if all( [elem!=0 for elem in self.GPSLastKnownCoord] ):
                            self.Latitude = self.GPSLastKnownCoord[0]
                            self.Longitude = self.GPSLastKnownCoord[1]
                            self.LocationSource = "GPS"
                        else:
                            self.Latitude = self.NetworkLastKnownCoord[0]
                            self.Longitude = self.NetworkLastKnownCoord[1]
                            self.LocationSource = "Network"
                    #END IF

                #END IF/ELSE
                #After all of this parsing, we just need to set anything that is empty to N/A
                emptiesToSet = ["Server", "Host", "WiFiBSSID", "WiFiSSID"]
                self.setEmptysToDefault(attributes=emptiesToSet)
            #END IF
            elif self.ClientType == "Desktop":
                #Read in Operating System Header Information
                self.parseLineAndSetAttr(fileStream=fs, delimiter="OS: ", attribute="", hasParts=True,
                                            subDelims=["Name =", "Architecture ="],
                                            subAttrs=["OSName", "OSArchitecture"] )
                self.parseLineAndSetAttr(fileStream=fs, delimiter="Version:", attribute="OSVersion")
                #PhoneAPIVer will hold the OS version, which is in OSName (for Windows) or OSVersion (Mac)
                # and will be used later to facilitate easier CSV creation
                self.PhoneAPIVer = self.OSName if ("Windows" in self.OSName) else self.OSVersion

                #Setting Location Source. On Desktops, it's always from an IP address
                self.LocationSource = "IP Address"

                #Get Network Provider
                self.parseLineAndSetAttr(fileStream=fs, delimiter="Network ISP:", attribute="NetworkProvider")

                #Setting Environment based on OSName
                if "Windows" in self.OSName:
                    self.Environment = "Windows PC"
                if "Mac" in self.OSName:
                    self.Environment = "Mac OS X"

                #Get the Latitude and Longitude
                self.parseLineAndSetAttr(fileStream=fs, delimiter="IPLastKnownLat:", attribute="Latitude")
                self.parseLineAndSetAttr(fileStream=fs, delimiter="IPLastKnownLng:", attribute="Longitude")

                #Getting all of the Connection Types and Connection Names
                self.ConnectionName  = []
                self.ConnectionType  = []
                line = "placeholder"
                while line:
                    #If "ConnectionName" is in the line, then we grab the value, and
                    # go to the next line, which will contain the Connection Type
                    if "ConnectionName:" in line:
                        self.ConnectionName.append(line.split("ConnectionName:")[1].strip())
                        line = fs.readline()
                        self.ConnectionType.append(line.split("ConnectionType:")[1].strip())
                    line = fs.readline()
                #END WHILE

                #After all of this parsing, we just need to set anything that is empty to N/A
                emptiesToSet = ["JavaVersion", "JavaVendor", "Server", "Host",
                                "NetworkOperator", "NetworkType", "Roaming", "PhoneModel",
                                "PhoneManufac", "PhoneSDKVer","WiFiBSSID", "WiFiSSID", "DistanceMoved" ]
                self.setEmptysToDefault(attributes=emptiesToSet)
            #END IF/ELIF
        #END WITH FILE
    #END DEF

    def __getLocationCoords(self, fileStream, typ=""):
        """
        A function used by loadCrowdSourceInfo to parse for multiple location coordinates
        in the file based on type (everything, GPS, or Network)
        """
        if typ not in ["", "GPS", "Network"]:
            raise ValueError("Your type of Location values were not one of the options:"+str(["", "GPS", "Network"]))
        #Now we will look for the specified types of Location information
        latitudes = getLinesWith(fileStream, typ+"Latitude:")
        longitudes = getLinesWith(fileStream, typ+"Longitude:")
        distsMoved = getLinesWith(fileStream, typ+"DistanceMoved:")

        pairs = []
        #Now we are going to go through our three arrays, grabbing each value
        # and making a 3-element array out of the latitude, longitude, and distance moved
        #We will only go along the array up to the shortest array so that we don't try to
        # index beyond the array
        for i in range( min([len(latitudes),len(longitudes),len(distsMoved)]) ):
            pairs.append( [latitudes[i].split(typ+"Latitude:")[1].strip(),
                           longitudes[i].split(typ+"Longitude:")[1].strip(),
                           distsMoved[i].split(typ+"DistanceMoved:")[1].strip()] )
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
                #END IF
            #END FOR
        #END IF
    #END DEF


# Creating values for CSV ----------------------------------------------------------------------

    def get_csvDefaultValues(self, **kwargs):
        defaultVals = []
        defaultVals.append( self.Date )
        defaultVals.append( self.Time )
        defaultVals.append( self.AppVersion )
        defaultVals.append( self.Environment )
        defaultVals.append( self.PhoneModel )
        defaultVals.append( self.PhoneManufac )
        defaultVals.append( self.PhoneAPIVer )
        defaultVals.append( self.PhoneSDKVer )
        defaultVals.append( self.NetworkProvider )
        defaultVals.append( self.NetworkOperator )
        #If the device was a desktop, then we want the Network
        # column in the CSV to hold all of the connection types the
        # device had
        if self.ClientType == "Desktop":
            connTypes = ""
            for typ in self.ConnectionType:
                connTypes += typ+", "
            defaultVals.append( connTypes[:-2] )
        else:
            if self.NetworkType.lower() == "wifi":
                defaultVals.append( self.NetworkType )
            else:
                defaultVals.append( self.ConnectionType )
            #END IF/ELSE
        #END IF/ELSE
        if self.Roaming:
            defaultVals.append( "Roaming" )
        else:
            defaultVals.append( "Not Roaming" )
        defaultVals.append( self.WiFiBSSID )
        defaultVals.append( self.WiFiSSID )
        defaultVals.append( self.LocationSource )
        defaultVals.append( self.Latitude )
        defaultVals.append( self.Longitude )
        defaultVals.append( self.DistanceMoved )
        defaultVals.append( self.ClientType )
        return defaultVals
    #END DEF

    def get_csvExtraValues(self):
        #csvExtraHeaders = []
        extraVals = []
        #extraVals.append( self.AvgLatitude )
        #extraVals.append( self.AvgLongitude )
        return extraVals
    #END DEF

    def _get_csvValues(self, typ, vals, count):
        """
        This takes a type of CSV values to get from a test type (typ) the values
          requested (vals).
        ARGS:
            typ     String, the type of test we want get values from
            vals    String, the kind of values want to from the tests
            count   Integer, the expected number of values returned
        """
        if typ not in ["TCP","UDP", "PING"]:
            raise ValueError("We cannot get values from the type of test you requested.\n"+
                            "The type must be one of the following: "+str(["TCP","UDP", "PING"]))
        if typ=="TCP" and vals not in ["Default","Stat","Qual"]:
            raise ValueError("We cannot get the type of values you requested.\n"+
                            "The type must be one of the following: "+str(["Default","Stat","Qual"]))
        if typ=="UDP" and vals not in ["Default"]:
            raise ValueError("We cannot get the type of values you requested.\n"+
                            "The type must be one of the following: "+str(["Default"]))
        if typ=="PING" and vals not in ["Default","RvMos"]:
            raise ValueError("We cannot get the type of values you requested.\n"+
                            "The type must be one of the following: "+str(["Default","RvMos"]))
        #END PRE-CONDITIONS

        returnVals = []
        #This will get all of the West values, and then the East values
        for connLoc in ["West", "East"]:
            tests = self.getTest(typ, ConnectionLoc=connLoc)
            try:
                returnVals.extend( getattr(tests[0],"get_csv"+vals+"Values")() )
            except:
                returnVals.extend( [self.ErrorTypes[self.ErrorCode]]*count )
            #END IF/ELSE
        #END FOR
        return returnVals
    #END DEF

    def get_csvPINGValues(self):
        return self._get_csvValues("PING", "Default", 4)
    #END DEF

    def get_csvUDPValues(self):
        return self._get_csvValues("UDP", "Default", 3)
    #END DEF

    def get_csvTCPValues(self):
        return self._get_csvValues("TCP", "Default", 2)
    #END DEF

    def get_csvStatValues(self):
        return self._get_csvValues("TCP", "Stat", 4)
    #END DEF

    def get_csvQualValues(self):
        return self._get_csvValues("TCP", "Qual", 4)
    #END DEF

    def get_csvRvMosValues(self):
        return self._get_csvValues("PING", "RvMos", 2)
    #END DEF


# String printout ------------------------------------------------------------------------------

    # DESC: Returns a string representation of the object
    def __str__(self):
        """Returns a string represenation of the object"""
        string = (self.StringPadding +
                    "Filename: " + str(self.Filename) +"\n"+
                  self.StringPadding +
                    "DateTime of Speed Test: " + str(self.Date) +" "+ str(self.Time) +"\n"+
                  self.StringPadding +
                    "Client Type: " + str(self.ClientType) +"\n"+
                  self.StringPadding +
                    "App Version: " + str(self.AppVersion) +"\n"+
                  self.StringPadding +
                    "Location Source: " + str(self.LocationSource) +"\n"+
                  self.StringPadding +
                    "Location: (" + str(self.Latitude) +","+ str(self.Longitude) +")\n"+
                  self.StringPadding +
                    "Distance Moved: " + str(self.DistanceMoved) +"\n"
                 )
        if self.ClientType == "Phone":
            string += (self.StringPadding +
                            "OS: " + str(self.OSName) +", "+ str(self.OSArchitecture) +
                              ", "+ str(self.OSVersion) +"\n"+
                       self.StringPadding +
                            "Java: " + str(self.JavaVersion) +", "+ str(self.JavaVendor) +"\n"+
                       self.StringPadding +
                            "Connection: Server = " + str(self.Server) +
                              ", Host = "+ str(self.Host) +"\n"+
                       self.StringPadding +
                            "Network: Provider = " + str(self.NetworkProvider) +
                              ", Operator = "+ str(self.NetworkOperator) +"\n"+
                       self.StringPadding +
                            "Connection Type: " + str(self.ConnectionType) +"\n"+
                       self.StringPadding +
                            "Roaming: " + repr(self.Roaming) +"\n"+
                       self.StringPadding +
                            "Environment: " + str(self.Environment) +"\n"+
                       self.StringPadding +
                            "Phone: Model = " + str(self.PhoneModel) +
                              ", Manufacturer = " + str(self.PhoneManufac) +"\n"+
                       self.StringPadding +
                            "Phone: API version = " + str(self.PhoneAPIVer) +
                              ", SDK version = " + str(self.PhoneSDKVer) +"\n"+
                       self.StringPadding +
                            "WiFi: BSSID = " + str(self.WiFiBSSID) +
                              ", SSID = " + str(self.WiFiSSID) +"\n"
                      )
        elif self.ClientType == "Desktop":
            string += (self.StringPadding +
                            "OS: " + str(self.OSName) +", "+ str(self.OSArchitecture) +
                              ", " + str(self.OSVersion) +"\n"+
                       self.StringPadding +
                            "Network ISP: "+ str(self.NetworkProvider) +"\n")
            #This will loop through all of the Connections, printing out
            # their name and type
            for key, val in enumerate(self.ConnectionName):
                string += (self.StringPadding +
                                "Connection "+str(key)+": Name =  "+ str(val) +", "+
                                "Type = "+ str(self.ConnectionType[key]) +"\n" )
            #END FOR
        #END IF/ELIF
        string += (self.StringPadding +
                        "Contain Major Errors: " + repr(self.ContainsErrors) +"\n"+
                        ((self.StringPadding + \
                            "Error Type: " + self.ErrorTypes[self.ErrorCode] + "\n") \
                          if self.ContainsErrors else "" ) +
                        ((self.StringPadding + \
                            "Error Message: " + self.ErrorMessages[self.ErrorCode] + "\n") \
                          if self.ContainsErrors else "" ) +
                    self.printTests()
                  )
        return string
    #END DEF

    '''
    def __repr__(self):
        """Returns a string of all of the attributes in this object"""
        string = ""
        for elem in self.__dict__:
            if "__" not in elem and elem[0] != "_":
                string += elem+":   "+str(self.__dict__[elem])+"\n"
        return string
    #END DEF
    '''
#END CLASS
