"""
------------------------------------------------------------------------
_FILE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will hold a raw data file's header information (see list of variables)
            and then parses individual tests from the remaining text, storing them as a series of
            objects in the Tests variable

VARIABLES:
    ObjVersion      Float, the version that this object is in development
    FilePath        String, holds the full path to the text file being parsed
    Filename        String, holding file name that is being parsed
    Date            String, holding the date the test was taken
    Time            String, holding the time test was taken
    EastWestSrvr    Tuple of two Strings, first String is the IP address of the East server, second the West
    Tests           Dictionary, holds all of the speed tests (TCP, UDP, PING, or TCRT) that have been parsed.
                      Note: the NUM key holds a List of all tests (TCP, UDP, PING & TCRT),
                      with their TestNumber as the key

FUNCTIONS:
  INITIALIZATION
    __init__ - initializes the object by parsing the data in the given file path
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
                    filePath:   String, containing absolute path to raw data file
        OUTPUTS-    none
    loadHeaderInfo - initializes the object by parsing the data in the given file path.
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    parseLineAndSetAttr - Takes a file stream, and parses a specific line, gets the necessary values
                from the line, and sets them in the object. If the object does not have the specified
                variable (i.e. attribute is not specified in the class or __init__), then the function
                will create the variable
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    setEmptysToDefault - After loading header information, sets any empty values to "N/A"
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None

  PARSING TESTS
    findAndParseTCPTests - This takes the contents of the file being parsed, splits the content by "Staring Test"
                (to included any error messages in the tests) and the creates the TCP Test objects.
                Assumes that self._fileContentsByTest contains all of the tests
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    findAndParsePINGTests - This takes the contents of the file being parsed, splits the content by "Staring Test"
                (to included any error messages in the tests) and the creates the PING Test objects.
                Assumes that self._fileContentsByTest contains all of the tests
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    findAndParseTCRTTests - This takes the contents of the file being parsed, splits the content by "Staring Test"
                (to included any error messages in the tests) and the creates the TCRT Test objects.
                Assumes that self._fileContentsByTest contains all of the tests
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None
    readAllTestsFromFile - Reads all of the content from self.FilePath, splits it by "Starting Test", and
                stores the resulting tests in self._fileContentsByTest. If the length of
                self._fileContentsByTest is 1, then there was a problem connecting, and we
                set self._contains_Errors to True.
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    None

  GETTERS
    getTest - Gets the object that meets the specified values. Type of test (PING, TCP, or UDP) must
                be given, but all other attributes must be given through keyword arguments
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
                    testType:   String, the type of test that will be searched for
                    kwargs:     Strings, the attributes that the test must have.
        OUTPUTS-    List of type _Test objects that meet the specified attributes in kwargs

  STRING PRINTOUT:
    printTests - Return a string that has the information of each speed test in the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    text:   String, a representation of the IndividualSpeedTests held in
                            this objects mySpeedTests
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
------------------------------------------------------------------------
"""


# IMPORTS
#Importing necessary data_utils functions
from PyObjects.utils.basic_utils import (getFirstLineWith, monthAbbrToNum,
                                        calcTCPThroughput, calc_rVal_MOS)
#Import some global vars from data_utils
from PyObjects.__Base import (Formatting, ErrorHandling)
#Importing the different kinds of tests from their respective modules
from PyObjects.TCP_Test import TCP_Test
#UDP Tests are outputed slightly differently among different file types,
# so we'll let them specify how to differentiate and store them
#from PyObjects.UDP_Test import UDP_Test
from PyObjects.PING_Test import PING_Test
from PyObjects.TCRT_Test import TCRT_Test
#END IMPORTS

# CLASS
class File(Formatting, ErrorHandling):
    # ------------------------------
    # Class attributes
    FilePath    = ""
    Filename    = ""
    Date        = ""
    Time        = ""
    EastWestSrvr = None
    Tests       = None
    TestsByNum  = None
    _fileContentsByTest = None
    # ------------------------------

    # DESC: init functions calls load using the given file path
    def __init__(self, filePath="", eastWest=("0.0.0.0", "0.0.0.0")):
        Formatting.__init__(self)
        ErrorHandling.__init__(self)
        self.ObjVersion = 0.9
        self.Tests = { "TCP" : [],
                       "UDP" : [],
                       "PING": [],
                       "TCRT" : [] }
        self.TestsByNum = {}
        self.FilePath = filePath
        self.EastWestSrvr = eastWest
        self.Filename = self.FilePath.split("/")[-1]
        self.loadHeaderInfo()
    #END INIT


# Initialization functions ---------------------------------------------------------------------

    # DESC: parses data and info in given file (location is filePath)
    #       and stores it in the object's attributes
    def loadHeaderInfo(self):
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath) as fs:
            #Reading in the Date and Time of the test
            datetime = getFirstLineWith(fs, "Testing started at")
            #If we were returned something, then we need to parse the date and time
            if datetime:
                datetime = datetime.split("Testing started at")[1]
                #Removing the day of the week from the remaining text
                datetime = datetime[4:-1].strip()
                #Determining the Month, Day, and Time from the first part of the text
                monthName = datetime[:3]
                month = str(monthAbbrToNum(monthName))
                datetime = datetime.split(monthName)[1].strip()
                day = str(datetime[:2])
                datetime = datetime[2:].strip()
                time = str(datetime[:8])
                datetime = datetime[8:].strip()
                #The year cannot be assumed to be in the same place, in the same format, so we
                # will split on " 20", and the next two characters must be the suffix
                year = "20" + datetime.split(" 20")[1][:2]
                self.Date = month + "/" + day + "/" + year
                self.Time = time
            else:
                #I can't use the getFirstLineWith function as I do not know what I'm looking for exactly,
                # so I'll have to do some regular expression searching
                #Reading in a chunk of text
                allText = fs.read(100)
                #Splitting based on newline characters
                topChunk = allText.split("\n")[:5]
                from re import search
                datetime = ""
                for line in topChunk:
                    #Searches for a line which contains any two characters at the start
                    # of a line (hopefully numbers), then a forward slash "/", then two more
                    # characters, then another "/", and then two more characters. Hopefully, the
                    # only line that has this kind of string is the one that contains
                    # the date and time
                    if search("^../../..", line):
                        datetime = line
                        break
                #END FOR
                self.Date = datetime.split(" ")[0].strip()
                self.Time = datetime.split(" ")[1].strip()
            #END IF/ELSE
        #END WITH FILE
    #END DEF

    # DESC: Takes a file stream, and parses a specific line, gets the necessary values
    #       from the line, and sets them in the object. If the object does not have the specified
    #       variable (i.e. attribute is not specified in the class or __init__), then the function
    #       will create the variable
    def parseLineAndSetAttr(self, fileStream, delimiter, attribute, hasParts=False, **kwargs):
        #First, try to read from the file, to check if it is an actual file stream
        try:
            __ = fileStream.read(1)
            fileStream.seek(0)
        except:
            raise ValueError("You have not passed through an open file stream")
        #Now that we know we have an open file stream, we can perform the parsing function.
        #But first, we check that the delimiter is a string
        if not isinstance(delimiter, str):
            raise ValueError("The delimiter must be a string")
        #We check the variable hasParts, which is set to true if there are parts of the line that
        # hold separate values, like the OS and Java information in Phone versions of this testing
        line = getFirstLineWith(fileStream, delimiter)
        #If there is something in line, then we parse it out. Otherwise, the function is done, and
        # nothing is set that wasn't there
        if line:
            if not hasParts:
                value = line.split(delimiter)[1].strip()
                if not value:
                    value = "NA"
                self.__dict__[attribute] = value
            else:
                #We need to check that the necessary keyword arguements have been passed through
                # the function if hasParts was set to True
                if "subDelims" not in kwargs.keys():
                    raise KeyError("You did not pass the necessary keyword arg through the function.\n" +
                                    "Missing: subDelims. Is a: List of sub-delimiters")
                if not isinstance(kwargs["subDelims"], list):
                    raise TypeError("You did not pass the necessary keyword arg through the function.\n" +
                                    "Attr: subDelims. Was not a: List of sub-delimiters")
                if "subAttrs" not in kwargs.keys():
                    raise KeyError("You did not pass the necessary keyword arg through the function.\n" +
                                    "Missing: subAttrs. Is a: List of attributes to set")
                if not isinstance(kwargs["subAttrs"], list):
                    raise TypeError("You did not pass the necessary keyword arg through the function.\n" +
                                    "Attr: subAttrs. Was not a: List of attributes to set")
                if len(kwargs["subAttrs"]) != len(kwargs["subDelims"]):
                    raise ValueError("subDelims and subAttrs must have the same number of values")
                #END IFs
                #Now we are going to loop through each sub-delimiter, splitting the string on it. We also
                # keep track of what it's index is. The value parsed is then put into the variable
                # name from the tuple in subAttrs at the same index.
                for key, delimiter in enumerate(kwargs["subDelims"]):
                    value = line.split(delimiter)[1].split(",")[0].strip()
                    if not value:
                        value = "NA"
                    self.__dict__[kwargs["subAttrs"][key]] = value
                #END FOR
            #END IF/ELSE
        #END IF
    #END DEF

    # DESC: After loading header information, sets any empty values to "N/A"
    def setEmptysToDefault(self, attributes):
        if not isinstance(attributes, list):
            raise TypeError("The attributes argument must be a List of attributes in the class.")
        for elem in attributes:
            try:
                self.__dict__[elem] = "NA" if not self.__dict__[elem] else self.__dict__[elem]
            except KeyError:
                self.__dict__[elem] = "NA"
            except:
                raise RuntimeError("Something went wrong trying to set '"+elem+"' in this object")
            #END TRY/EXCEPT
        #END FOR
    #END DEF


# Test Parse functions --------------------------------------------------------------------------

    # DESC: This takes the contents of the file being parsed, splits the content by "Staring Test"
    #       (to included any error messages in the tests) and the creates the TCP Test objects.
    #       Assumes that self._fileContentsByTest contains all of the tests
    def findAndParseTCPTests(self):
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                if "TCP" in chunk:
                    try:
                        #The chunk holds a TCP Test, so we pass it to the constructor, and then
                        # append the test to our tests. We append in two places; in the TCP category
                        # and in the NUM category (inserted at the index that corresponds to the test number)
                        #The if statement is one last check to make sure that the test actually contains
                        # some basic information
                        if "Iperf command line" in chunk:
                            parsedTest = TCP_Test(dataString=chunk, eastWest=self.EastWestSrvr)
                            self.Tests[parsedTest.ConnectionType].append(parsedTest)
                            self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                        #END IF
                    except:
                        raise RuntimeError("Something went wrong when trying to put the TCP test into this "+
                                           "File object.\nFilePath: "+self.FilePath)
                    #END TRY/EXCEPT
                #END IF
            #END FOR
        #END IF
    #END DEF

    # DESC: This takes the contents of the file being parsed, splits the content by "Staring Test"
    #       (to included any error messages in the tests) and the creates the PING Test objects.
    #       Assumes that self._fileContentsByTest contains all of the tests
    def findAndParsePINGTests(self):
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                #This is checking if any of the strings in the above list are present
                # in the current chunk. We then check if the string "Checking Connectivity"
                # is not in the chunk. If it's not, then we have a Ping test
                possibleStrings = ["Ping", "ping", "PING"]
                isAPingTest = any( [(string in chunk) for string in possibleStrings] )
                if ( isAPingTest and ("Checking Connectivity" not in chunk) ):
                    try:
                        #The chunk holds a PING Test, so we pass it to the constructor, and then
                        # append the test to our tests. We append in two places; in the PING category
                        # and in the NUM category (inserted at the index that corresponds to the test number)
                        parsedTest = PING_Test(dataString=chunk, eastWest=self.EastWestSrvr)
                        self.Tests[parsedTest.ConnectionType].append(parsedTest)
                        self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                        #END IF
                    except:
                        raise RuntimeError("Something went wrong when trying to put the PING test into this "+
                                           "File object.\nFilePath: "+self.FilePath)
                    #END TRY/EXCEPT
                #END IF
            #END FOR
        #END IF
    #END DEF

    # DESC: This takes the contents of the file being parsed, splits the content by "Staring Test"
    #       (to included any error messages in the tests) and the creates the TCRT Test objects.
    #       Assumes that self._fileContentsByTest contains all of the tests
    def findAndParseTCRTTests(self):
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                #Making sure that the chunk is a traceroute test
                if any( [(string in chunk) for string in ["traceroute", "Traceroute"]] ):
                    try:
                        #The chunk holds a TRACERT Test, so we pass it to the constructor, and then
                        # append the test to our tests. We append in two places; in the TRACRT category
                        # and in the NUM category (inserted at the index that corresponds to the test number)
                        parsedTest = TCRT_Test(dataString=chunk, eastWest=self.EastWestSrvr)
                        self.Tests[parsedTest.ConnectionType].append(parsedTest)
                        self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                    except:
                        raise RuntimeError("Something went wrong when trying to put the TCRT test into this "+
                                           "File object.\nFilePath: "+self.FilePath)
                    #END TRY/EXCEPT
                #END IF
            #END FOR
        #END IF
    #END DEF

    # DESC: Reads all of the content from self.FilePath, splits it by "Starting Test", and
    #       stores the resulting tests in self._fileContentsByTest. If the length of
    #       self._fileContentsByTest is 1, then there was a problem connecting, and we
    #       set self._contains_Errors to True.
    def readAllTestsFromFile(self):
        #This is a check to see if the function has already run and found an
        # error in the output. This way, we don't unnecessarily run the function again
        if not self.ContainsErrors and self._fileContentsByTest == None:
            #We need to first open the file, and read all of the contents into one big string
            with open(self.FilePath) as fs:
                allText = fs.read()
            #END WITH FILE
            if "Connectivity Test Failed" in allText and "Starting Test" not in allText:
                self.ContainsErrors = True
                self.ErrorCode = 311
                return
            #First splitting the contents into sections. These sections are all of the areas
            # bounded by a "Starting Test"
            self._fileContentsByTest = allText.split("Starting Test")
            if len(self._fileContentsByTest) == 1:
                self.ContainsErrors = True
                self.ErrorCode = 310
                return
            #END IF
            #Re-appending "Starting Test" to all of the chunks of text output
            self._fileContentsByTest = [("Starting Test" + chunk) for chunk in self._fileContentsByTest[1:]]
        #END IF
    #END DEF


# Getters -----------------------------------------------------------------------------------

    # DESC: Get the object that meets the specified values
    def getTest(self, testType, **kwargs):
        #Checking that the type is one of the possible types
        if testType not in self.Tests.keys():
            raise ValueError("The \"testType\" was not of the possible types. "+str(self.Tests.keys()))
        #If no other attributes were passed in through kwargs, then we just return all
        # of the test of that type
        if len(kwargs) == 0:
            return self.Tests[testType]
        #Otherwise, we will go through all of the tests, and find the ones that have
        # the specified attributes.
        else:
            matchingTests = []
            for test in self.Tests[testType]:
                matchesAll = True
                #This will go through all of the key/value pairs in kwargs, and test
                # if the test has the attributes. If any are found to not match, then
                # the boolean is set to false, and the test will not be added to the
                # returning array. If the test does not have the attribute at all, then
                # the boolean is set to false, and the test is not added.
                for key, value in kwargs.items():
                    try:
                        if test.__dict__[key] != value:
                            matchesAll = False
                            break
                    #This except block will run if the test did not have the attribute "key",
                    # as test.__dict__[key] will cause a KeyError
                    except:
                        matchesAll = False
                        break
                #END FOR
                if matchesAll:
                    matchingTests.append(test)
            return matchingTests
    #END DEF


# String printout ----------------------------------------------------------------------------

    # DESC: Returns all of the sub tests for this file as a string. If there are no
    #       tests, then it returns a string saying there were no tests
    def printTests(self):
        text = ""
        testNumKeys = list(self.TestsByNum.keys()); testNumKeys.sort()
        for aTestNum in testNumKeys:
            text += str(self.TestsByNum[aTestNum])
        #END FOR
        if text == "":
            text = self.StringPadding + "No viable network speed tests\n"
        return text
    #END DEF

    # DESC: Returns a string representation of the object
    def __str__(self):
        return (self.StringPadding +
                    "Filename: " + str(self.Filename) + "\n" +
                self.StringPadding +
                    "DateTime of Speed Test: " + str(self.Date) + " " + str(self.Time) + "\n" +
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
