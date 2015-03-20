"""
------------------------------------------------------------------------
_FILE.PY

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
from datetime import datetime
#Importing necessary basic_utils functions
from parserUtils.basic_utils import (getLinesWith, monthAbbrToNum)
#Importing the necessary abstract classes and sub-classes
from __Base import (Formatting, ErrorHandling)
from TCP_Test import TCP_Test
from UDP_Test import UDP_Test
from PING_Test import PING_Test
from TCRT_Test import TCRT_Test
#END IMPORTS


class File(Formatting, ErrorHandling):

    """
    An abstract class that is the basis of the objects returned to a user
     asking for a file to be parsed.
    Inheritted by FieldTest_File and CrowdSource_File
    """

    '''
    # ------------------------------
    # ---- CLASS ATTRIBUTES ----
    FilePath        = ""
    Filename        = ""
    Date            = ""
    Time            = ""
    EastWestSrvrIPs = None
    Tests           = None
    TestsByNum      = None
    _fileContentsByTest = None
    # ------------------------------
    '''



    def __init__(self, filePath="", eastWestIP=("0.0.0.0", "0.0.0.0")):
        """
        Initializes the object by parsing the data in the given file path
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            filePath:   String, containing absolute path to raw data file
            eastWest:   Tuple of Strings, the IP addresses of the East and West server
        """
        #Calling Formatting and ErrorHandling's initialization
        Formatting.__init__(self)
        ErrorHandling.__init__(self)
        #To be updated while the software improves??
        # May be used to determine whether an object was parsed with a specific
        # version of the software
        self.ObjVersion = 0.9
        self.Tests = { "TCP":[],
                       "UDP":[],
                       "PING":[],
                       "TCRT":[] }
        self.TestsByNum = {}
        self.FilePath = os.path.abspath(filePath)
        self.EastWestSrvrIPs = eastWestIP
        self.Filename = self.FilePath.split("/")[-1]
        self.loadHeaderInfo()
    #END INIT



# INITIALIZATION FUNCTIONS ---------------------------------------------------------------------

    def loadHeaderInfo(self):
        """Initializes the object by parsing the data in the given file path."""
        #This opens the file, and stores the file stream into the variabe fs
        with open(self.FilePath) as fs:
            #Reading in the Date and Time of the test
            datetime = getLinesWith(fs, "Testing started at")

            #If we were returned something, then we need to parse the date and time
            #
            # TODO : Use datetime objects
            #
            if datetime:
                datetime = datetime[0].split("Testing started at")[1]
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
                #I can't use the getLinesWith function as I do not know what I'm looking for exactly,
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

    def parseLineAndSetAttr(self, fileStream, delimiter, attribute, hasParts=False):
        """
        Takes a file stream, and parses a specific line, gets the necessary values
        from the line, and sets them in the object. If the object does not have the specified
        variable (i.e. attribute is not specified in the class or __init__), then the function
        will create the variable.
        """
        #First, try to read from the file, to check if it is an actual file stream
        try:
            __ = fileStream.read(1)
            fileStream.seek(0)
        except:
            raise ValueError("You have not passed through an open file stream")
        #Now that we know we have an open file stream, we can perform the parsing function.
        #But first, we check that the delimiter is a string
        if not isinstance(delimiter, str) and not hasParts:
            raise ValueError("The delimiter was {}, and must be a string.".format(type(delimiter)))
        if not isinstance(delimiter, list) and hasParts:
            raise ValueError("The delimiter was {}, and must be a list.".format(type(delimiter)))

        #We check the variable hasParts, which is set to true if there are parts of the line that
        # hold separate values, like the OS and Java information in Phone versions of this testing
        if not hasParts:
            #If there is something in line, then we parse it out. Otherwise, the function is done, and
            # nothing is set that wasn't there
            if attribute not in self.__dict__:
                self.__dict__[attribute] = ""
            line = getLinesWith(fileStream, delimiter)
            if line:
                value = line[0].split(delimiter)[1].strip()
                if not value:
                    value = "NA"
                self.__dict__[attribute] = value
        else:
            #We need to check that the necessary argument types have been passed through
            # the function if hasParts was set to True
            if not isinstance(attribute, list):
                raise TypeError("You need to pass in a LIST of attributes to set")
            if len(delimiter) != len(attribute):
                raise ValueError("'delimiter' and 'attribute' must have the same number of values")
            #END IFs
            #Now we are going to loop through each sub-delimiter, splitting the string on it. We also
            # keep track of what it's index is. The value parsed is then put into the variable
            # name from the tuple in subAttrs at the same index.
            for subDelimiter in delimiter:
                subDelimInd = delimiter.index(subDelimiter)
                #If there is something in line, then we parse it out. Otherwise, the function is done, and
                # nothing is set that wasn't there
                if attribute[subDelimInd] not in self.__dict__:
                    self.__dict__[attribute[subDelimInd]] = ""
                line = getLinesWith(fileStream, subDelimiter)
                if line:
                    value = line[0].split(subDelimiter)[1].strip().split(",")[0].strip()
                    if not value:
                        value = "NA"
                    self.__dict__[attribute[subDelimInd]] = value
            #END FOR
        #END IF/ELSE
    #END DEF

    def setEmptysToDefault(self, attributes):
        """After loading header information, sets any empty values to "N/A" """
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



# TEST PARSER FUNCTION --------------------------------------------------------------------------

    def __findAndParseTests(self, type_):
        """
        This takes the contents of the file being parsed, splits the content by "Staring Test"
         (to included any error messages in the tests) using the readAllTestsFromFile function,
         and the creates the specified Test objects. Assumes that self._fileContentsByTest
         contains all of the tests.
        """
        #First we run the readAllTestsFromFile function, to make sure that self._fileContentsByTest
        # is set, and contains all of the test output
        self.readAllTestsFromFile()
        #If the function above ran and did not hit any major errors, then we can run the code
        # inside of the IF block
        if not self.ContainsErrors:
            for chunk in self._fileContentsByTest:
                if type_ == "TCP":
                    parsedTest = TCP_Test(dataString=chunk, eastWestIP=self.EastWestSrvrIPs)
                if type_ == "UDP":
                    parsedTest = UDP_Test(dataString=chunk, eastWestIP=self.EastWestSrvrIPs)
                if type_ == "PING":
                    parsedTest = PING_Test(dataString=chunk, eastWestIP=self.EastWestSrvrIPs)
                if type_ == "TCRT":
                    parsedTest = TCRT_Test(dataString=chunk, eastWestIP=self.EastWestSrvrIPs)
                #If the line above returned an object (and not None), and the object's
                # ErrorCode is not 1, then we have correctly parsed a Test, and can
                # add it to our list.
                if parsedTest:
                    self.Tests[parsedTest.ConnectionType].append(parsedTest)
                    self.TestsByNum[int(parsedTest.TestNumber)] = parsedTest
                else:
                    pass #If we are passing, then the test was not a TCP test
                #END IF/ELSE
            #END FOR
        #END IF
    #END DEF

    def findAndParseTCPTests(self):
        """Calls a private function to find and parse all TCP tests"""
        self.__findAndParseTests("TCP")
    #END DEF

    def findAndParseUDPTests(self):
        """Calls a private function to find and parse all UDP tests"""
        self.__findAndParseTests("UDP")
    #END DEF

    def findAndParsePINGTests(self):
        """Calls a private function to find and parse all PING tests"""
        self.__findAndParseTests("PING")
    #END DEF

    def findAndParseTCRTTests(self):
        """Calls a private function to find and parse all TCRT tests"""
        self.__findAndParseTests("TCRT")
    #END DEF

    def readAllTestsFromFile(self):
        """
        Reads all of the content from self.FilePath, splits it by "Starting Test", and
        stores the resulting tests in self._fileContentsByTest. If the length of
        self._fileContentsByTest is 1, then there was a problem connecting, and we
        set self._contains_Errors to True.
        """
        #This is a check to see if the function has already run and found an
        # error in the output. This way, we don't unnecessarily run the function again
        if not self.ContainsErrors and "_fileContentsByTest" not in self.__dict__:
            #We need to first open the file, and read all of the contents into one big string
            with open(self.FilePath) as fs:
                allText = fs.read()
            #END WITH FILE
            if "Connectivity Test Failed" in allText and "Starting Test" not in allText:
                self._ErrorHandling__setErrorCode(311)
                return
            #First splitting the contents into sections. These sections are all of the areas
            # bounded by a "Starting Test"
            self._fileContentsByTest = allText.split("Starting Test")
            if len(self._fileContentsByTest) == 1:
                self._ErrorHandling__setErrorCode(310)
                return
            #END IF
            #Re-appending "Starting Test" to all of the chunks of text output
            self._fileContentsByTest = [("Starting Test" + chunk) for chunk in self._fileContentsByTest[1:]]
        #END IF
    #END DEF



# ATTRIBUTE GETTERS -------------------------------------------------------------------------

    def getTest(self, type_, **kwargs):
        """
        Gets the object that meets the specified values. Type of test (PING, TCP, or UDP) must
        be given, but all other attributes must be given through keyword arguments
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            type_:      String, the type of test that will be searched for
            kwargs:     Strings, the attributes that the test must have.
        RETURNS:
            List of type _Test objects that meet the specified attributes in kwargs
        """
        #Checking that the type is one of the possible types
        if type_ not in self.Tests.keys():
            raise ValueError("The \"type_\" was not of the possible types. "+str(self.Tests.keys()))
        #If no other attributes were passed in through kwargs, then we just return all
        # of the test of that type
        if len(kwargs) == 0:
            return self.Tests[type_]
        #Otherwise, we will go through all of the tests, and find the ones that have
        # the specified attributes.
        else:
            matchingTests = []
            for test in self.Tests[type_]:
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



# STRING PRINTOUT ----------------------------------------------------------------------------

    def printTests(self):
        """
        Returns all of the sub tests for this file as a string. If there are no
        tests, then it returns a string saying there were no tests
        """
        text = ""
        testNumKeys = sorted(list(self.TestsByNum.keys()))
        for aTestNum in testNumKeys:
            text += str(self.TestsByNum[aTestNum])
        #END FOR
        if text == "":
            text = self.StringPadding + "No viable network speed tests\n"
        return text
    #END DEF

    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding +
                "Filename: {}\n".format(self.Filename) +
                self.StringPadding +
                "DateTime of Speed Test: {} {}\n".format(self.Date,self.Time) +
                self.StringPadding +
                "Contain Major Errors: {}\n".format(repr(self.ContainsErrors)) +
                ((self.StringPadding + "Error Type: " +self.ErrorType+ "\n")
                 if self.ContainsErrors else ""
                 ) +
                ((self.StringPadding + "Error Message: " +self.ErrorMessage+ "\n")
                 if self.ContainsErrors else ""
                 ) +
                self.printTests()
                )
    #END DEF


# COMPARISONS ----------------------------------------------------------------------------

    def __sameType(func):
        def wrapper(*args, **kwargs):
            if not isinstance(args[1], args[0].__class__):
                raise TypeError("You must compare the same type of object.\n"+
                                "Was given: "+str(type(args[0]))+" & "+str(type(args[1])))
            return func(*args, **kwargs)
        return wrapper
    #END DEF

    @__sameType
    def __lt__(self, object):
        #This will use the datetime module to create a datetime object from the
        # Date and Time variables. The datetime object will be used in comparisons
        __my_datetime = datetime.strptime(self.Date+" "+self.Time, "%m/%d/%Y %H:%M:%S")
        __other_datetime = datetime.strptime(object.Date+" "+object.Time, "%m/%d/%Y %H:%M:%S")
        return __my_datetime < __other_datetime
    @__sameType
    def __eq__(self, object):
        from datetime import datetime
        __my_datetime = datetime.strptime(self.Date+" "+self.Time, "%m/%d/%Y %H:%M:%S")
        __other_datetime = datetime.strptime(object.Date+" "+object.Time, "%m/%d/%Y %H:%M:%S")
        return __my_datetime == __other_datetime


    def __gt__(self, object):
        return (not self.__lt__(object) and not self.__eq__(object))
    def __ne__(self, object):
        return not self.__eq__(object)
    def __le__(self, object):
        return (self.__lt__(object) or self.__eq__(object))
    def __ge__(self, object):
        return (self.__gt__(object) or self.__eq__(object))

    @__sameType
    def __cmp__(self, object):
        if self.__lt__(object):
            return -1
        elif self.__eq__(object):
            return 0
        else:
            return 1
#END CLASS
