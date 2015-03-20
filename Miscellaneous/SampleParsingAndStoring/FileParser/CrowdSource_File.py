"""
------------------------------------------------------------------------
CROWDSOURCE_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import os
import sys
from platform import system
if system()=="Windows":
    import ntpath as path
else:
    import os.path as path
if path.dirname(__file__) not in sys.path:
    sys.path.append(path.dirname(__file__))

#Importing necessary basic_utils functions
from parserUtils.basic_utils import getLinesWith
#Importing the necessary base class
from _File import File
#Importing the senstive information
from _sensitiveInfo.serverIPs import CrowdSource_EastWest
#END IMPORTS


class CrowdSource_File(File):

    """
    The starting point for a user's interaction with the parser. This is the
    class that they import and initialize with a text file, containing the
    output of a Crowd Source test.
    """

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    FilePath    = ""
    Filename    = ""
    Date        = ""
    Time        = ""
    EastWestSrvr = (East IP, West IP)
    Tests       = {TCP, UDP, PING, NUM}
    TestsByNum  = {}
    _fileContentsByTest = None

    # ---- CLASS ATTRIBUTES ----
    Devicetype      = ""
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

    Roaming         = False
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

    #If Devicetype is "Desktop", these attributes are used for information
    # Devicetype
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
    '''



    def __new__(cls, *args, **kwargs):
        """
        Before creating an instance of the given file as a parsed object, we want to check
        that the file is indeed a test file. This will see if the necessary text
        is in the first few lines. If not, then we return None, and the object is not created
        """
        if 'empty' in kwargs and kwargs['empty']:
            return File.__new__(cls)
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
                allText = checkingFile.read()
            #END WITH FILE
            if all( [(string not in allText.split("\n\n")[0]) for string in ["Crowd Source"]] ):
                if "DEBUG" in kwargs and kwargs["DEBUG"]:
                    print("{} is not a Crowd Source Test output file. ".format(os.path.basename(fileLoc))+
                          "It did not have the necessary header.", file=sys.stderr)
                return None
            if allText.count("Starting Test") > 6:
                if "DEBUG" in kwargs and kwargs["DEBUG"]:
                    print("{} had too many tests conducted. ".format(os.path.basename(fileLoc))+
                          "It was most likely not a Crowd Source Test output file", file=sys.stderr)
                return None
        except:
            print("{} is a file that could not be read.".format(os.path.basename(fileLoc)), file=sys.stderr)
            return None
        inst = File.__new__(cls)
        return inst
    #END DEF

    def __init__(self, filePath="", **kwargs):
        """
        Initializes the object by parsing the data in the given file path. Calls parent's __init__
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            filePath:   String, containing absolute path to raw data file
        """
        if 'empty' in kwargs and kwargs['empty']:
            return
        #Quick little bit of formatting
        if system()!="Windows":
            filePath = path.abspath(filePath).replace("\\","").strip()

        #Call the parent class' __init__
        eastAndWestServerIP = CrowdSource_EastWest
        File.__init__(self, filePath=filePath, eastWestIP=eastAndWestServerIP)
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
            specialMessage = ("There was an unknown error of some kind, and the 14 necessary" +
                              " tests were not performed. There are "+str(6-len(self.TestsByNum))+
                              " tests missing.")
            self._ErrorHandling__setErrorCode(404, specialMessage)
        #END IF
    #END INIT



# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def loadCrowdSourceInfo(self):
        """Initializes the object by parsing the data in the given file path from __init__."""
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath,'r') as fs:
            #We are going to first get the line that contains some of the basic
            # information, like the Client Type and the App Version
            temp = getLinesWith(fs,"Crowd Source")
            if temp:
                if "Phone" in temp[0]:
                    self.Devicetype = "Phone"
                elif "Desktop" in temp[0]:
                    self.Devicetype = "Desktop"
                else:
                    self.Devicetype = "UNKNOWN"
                #END IF/ELIF/ELSE
                version = temp[0].split("v")[1].strip()
                self.AppVersion = "v"+version
            else:
                raise RuntimeError("This file is not a Crowd Source CPUC file.")
            #END IF/ELSE
            self.Roaming = False
            #If the device was a phone, then we will parse accordingly
            if self.Devicetype == "Phone":
                self.__loadPhoneInfo(fs)
            elif self.Devicetype == "Desktop":
                self.__loadDesktopInfo(fs)
            elif self.Devicetype == "UNKNOWN":
                emptiesToSet = ["Devicetype","AppVersion","OSName","OSArchitecture",
                                "OSVersion","JavaVersion","JavaVendor","Server","Host",
                                "NetworkProvider","NetworkOperator","NetworkType",
                                "ConnectionType","ConnectionName","Environment",
                                "PhoneModel","PhoneManufac","PhoneAPIVer","PhoneSDKVer",
                                "WiFiBSSID","WiFiSSID","LocationSource",
                                "Latitude","Longitude","DistanceMoved"]
                self.setEmptysToDefault(attributes=emptiesToSet)
            #END IF/ELIF
    #END DEF



# INITIALIZATION HELPERS -------------------------------------------------------

    def __loadPhoneInfo(self, fs):
            #Setting the values of our class variables
            #Read in Operating System Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter=["Name =", "Architecture =", ", Version ="],
                                     attribute=["OSName", "OSArchitecture", "OSVersion"],
                                     hasParts=True)
            #Read in Java Header Information
            self.parseLineAndSetAttr(fileStream=fs, delimiter=[": Version =", "Vendor ="],
                                     attribute=["JavaVersion", "JavaVendor"],
                                     hasParts=True)
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
            if line:
                self.Roaming = True
            line = getLinesWith(fs, "Network is Not Roaming.")
            if line:
                self.Roaming = False
            #Sometimes, there was a ":" in the output of the environment. This
            # little block below removes that
            self.Environment = self.Environment.replace(":","").strip()

            #The Latitude and Longitude information between app versions is different, so
            # we need to have separate blocks for each. The main difference is that v1.0 has
            # just Latitude and Longitude, while v1.1 and later have GPS Lat, GPS Long,
            # Network Lat, and NetworkLong
            self.LocationSource = ""
            self.DistanceMoved = 0
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
                if "Latitude" not in self.__dict__:
                    self.Latitude = 0
                    self.Longitude = 0
            #If the App Version is v1.1 or greater, then we have GPS Lat/Long and
            # Network Lat/Long.
            else:
                self.__loadPhoneCoords(fs)
            #After all of this parsing, we just need to set anything that is empty to N/A
            emptiesToSet = ["Server", "Host", "WiFiBSSID", "WiFiSSID"]
            self.setEmptysToDefault(attributes=emptiesToSet)
        #END IF
    #END DEF

    def __loadPhoneCoords(self, fs):
        self.AllGPSCoordPairs = self.__getLocationCoords(fileStream=fs, type_="GPS")
        self.AllNetworkCoordPairs = self.__getLocationCoords(fileStream=fs, type_="Network")
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
        for args_ in [(("GPSLastKnownLat:","GPSLastKnownLong:"), "GPSLastKnownCoord"),
                      (("NetworkLastKnownLat:","NetworkLastKnownLong:"), "NetworkLastKnownCoord")]:
            _getLastKnown(fs, args_[0], args_[1])
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
    #END DEF

    def __loadDesktopInfo(self, fs):
        #Read in Operating System Header Information
        self.parseLineAndSetAttr(fileStream=fs, delimiter=["Name =", "Architecture ="],
                                 attribute=["OSName", "OSArchitecture"],
                                 hasParts=True)
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
                        "NetworkOperator", "NetworkType", "PhoneModel",
                        "PhoneManufac", "PhoneSDKVer","WiFiBSSID", "WiFiSSID", "DistanceMoved" ]
        self.setEmptysToDefault(attributes=emptiesToSet)
    #END DEF

    def __getLocationCoords(self, fileStream, type_=""):
        """
        A function used by loadCrowdSourceInfo to parse for multiple location coordinates
        in the file based on type (everything, GPS, or Network)
        """
        if type_ not in ["", "GPS", "Network"]:
            raise ValueError("Your type of Location values were not one of the options:"+str(["", "GPS", "Network"]))
        #Now we will look for the specified types of Location information
        latitudes = getLinesWith(fileStream, type_+"Latitude:")
        longitudes = getLinesWith(fileStream, type_+"Longitude:")
        distsMoved = getLinesWith(fileStream, type_+"DistanceMoved:")

        pairs = []
        #Now we are going to go through our three arrays, grabbing each value
        # and making a 3-element array out of the latitude, longitude, and distance moved
        #We will only go along the array up to the shortest array so that we don't try to
        # index beyond the array
        for i in range( min([len(latitudes),len(longitudes),len(distsMoved)]) ):
            pairs.append( [latitudes[i].split(type_+"Latitude:")[1].strip(),
                           longitudes[i].split(type_+"Longitude:")[1].strip(),
                           distsMoved[i].split(type_+"DistanceMoved:")[1].strip()] )
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



# STRING PRINTOUT --------------------------------------------------------------

    def __phoneAsStr(self):
        return (self.StringPadding +
                "OS: {}, {}, {}\n".format(self.OSName,self.OSArchitecture,self.OSVersion) +
                self.StringPadding +
                "Java: {}, {}\n".format(self.JavaVersion,self.JavaVendor) +
                self.StringPadding +
                "Connection: Server = {}, ".format(self.Server) +
                "Host = {}\n".format(self.Host) +
                self.StringPadding +
                "Network: Provider = {}".format(self.NetworkProvider) +
                ", Operator = {}\n".format(self.NetworkOperator) +
                self.StringPadding +
                "Connection Type: {}\n".format(self.ConnectionType) +
                self.StringPadding +
                "Roaming: {}\n".format(repr(self.Roaming)) +
                self.StringPadding +
                "Environment: {}\n".format(self.Environment) +
                self.StringPadding +
                "Phone: Model = {}".format(self.PhoneModel) +
                ", Manufacturer = {}\n".format(self.PhoneManufac) +
                self.StringPadding +
                "Phone: API version = {}".format(self.PhoneAPIVer) +
                ", SDK version = {}\n".format(self.PhoneSDKVer) +
                self.StringPadding +
                "WiFi: BSSID = {}".format(self.WiFiBSSID) +
                ", SSID = {}\n".format(self.WiFiSSID)
                )
    #END DEF

    def __desktopAsStr(self):
        string = (self.StringPadding +
                  "OS: {}, {}, {}\n".format(self.OSName,self.OSArchitecture,self.OSVersion) +
                  self.StringPadding +
                  "Network ISP: {}\n".format(self.NetworkProvider))
        #This will loop through all of the Connections, printing out
        # their name and type
        for key, val in enumerate(self.ConnectionName):
            string += (self.StringPadding +
                       "Connection {}: Name = {}, ".format(key,val) +
                       "Type = {}\n".format(self.ConnectionType[key])
                       )
        #END FOR
        return string
    #END DEF

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (self.StringPadding +
                  "Filename: {}\n".format(self.Filename) +
                  self.StringPadding +
                  "DateTime of Speed Test: {} {}\n".format(self.Date,self.Time) +
                  self.StringPadding +
                  "Client Type: {}\n".format(self.Devicetype) +
                  self.StringPadding +
                  "App Version: {}\n".format(self.AppVersion) +
                  self.StringPadding +
                  "Location Source: {}\n".format(self.LocationSource) +
                  self.StringPadding +
                  "Location: ({},{})\n".format(self.Latitude,self.Longitude) +
                  self.StringPadding +
                  "Distance Moved: {}\n".format(self.DistanceMoved)
                  )
        if self.Devicetype == "Phone":
            string += self.__phoneAsStr()
        elif self.Devicetype == "Desktop":
            string += self.__desktopAsStr()
        #END IF/ELIF
        string += (self.StringPadding +
                   "Contain Major Errors: {}\n".format(repr(self.ContainsErrors)) +
                   ((self.StringPadding + " Error Type: {}\n".format(self.ErrorType))
                    if self.ContainsErrors else ""
                    ) +
                   ((self.StringPadding + " Error Message: {}\n".format(self.ErrorMessage))
                    if self.ContainsErrors else ""
                    ) +
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
