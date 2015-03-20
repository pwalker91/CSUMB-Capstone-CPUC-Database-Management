"""
------------------------------------------------------------------------
_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class is the bare bones for the TCP, UDP, and PING Test classes,
            as all test have different formats for their information, and
            different things that we want to track.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from __Base import (Formatting, ErrorHandling)
#END IMPORTS


class Test(Formatting, ErrorHandling):

    """An abstract Test class, which does some inital parsing and error checking"""

    '''
    # ------------------------------
    # ---- CLASS ATTRIBUTES ----
    #e.g. TCP, UDP
    ConnectionType  = ""
    #e.g. West, East
    ConnectionLoc   = ""

    Threads         = None
    TestNumber      = 0
    ReceiverIP      = ""
    Port            = 0000

    TestInterval    = 0
    MeasuringFmt    = None  #[kmKM] (Kbits, Mbits, KBytes, MBytes)
    _mform_short    = None
    _text           = ""
    iPerfCommand    = ""
    StartingLine    = ""
    # ------------------------------
    '''



    def __new__(cls, *args, **kwargs):
        """
        Before creating an instance of the given file as a parsed object, we want to check
        that the file is indeed a test file. This will see if the necessary text
        is in the first few lines. If not, then we return None, and the object is not created
        """
        #Getting the Data String passed to this constructor that was passed in to the constructor
        if "dataString" in kwargs:
            dataString = kwargs["dataString"]
        else:
            dataString = args[0]
        #END IF/ELSe
        if "Starting Test" not in dataString:
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (_Test) did not contain "+
                      "the necessary identifiers.",
                      file=sys.stderr)
            return None
        #END IF
        inst = object.__new__(cls)
        return inst
    #END DEF

    def __init__(self, dataString="", eastWestIP=("0.0.0.0", "0.0.0.0")):
        """
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the raw text that will be parsed
            eastWest:   Tuple of two Strings, first String is IP address of  East server, second is West
        """
        #Inheritting our formatting and error handling
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding * 2
        ErrorHandling.__init__(self)
        #Actual initialization
        self.TestNumber = 0
        self.iPerfCommand = ""
        self._text = dataString.split('\n')
        #This removes all lines that contain nothing
        self._text = [line for line in self._text if line]

        #This block will copy the command line call into the iPerfCommand variable,
        # as well as declare this objects TestNumber
        for line in self._text:
            if ("Starting Test" in line) and (self.TestNumber == 0):
                self.StartingLine = line
                rightChunk = self.StartingLine.split("Starting Test ")[1].strip()
                self.TestNumber = int(rightChunk.split(":")[0].split("..")[0])
            if "Iperf command line" in line:
                self.iPerfCommand = line
            if self.iPerfCommand != "" and self.TestNumber != 0:
                break
        #END FOR

        self.__setConnectionLoc(dataString, eastWestIP)
        self.__setIperfCommandOpts()

        self.__checkForError(dataString)
    #END DEF


    # INITIALIZATION HELPERS ---------------------------------------------------

    def __setConnectionLoc(self, dataString, EastWestIP):
        eastIP, westIP = EastWestIP
        if eastIP in dataString:
            self.ConnectionLoc = "East"
        elif westIP in dataString:
            self.ConnectionLoc = "West"
        else:
            if "West" in self.StartingLine:
                self.ConnectionLoc = "West"
            elif "East" in self.StartingLine:
                self.ConnectionLoc = "East"
            else:
                self.ConnectionLoc = "UNKNOWN"
            #END IF/ELIF/ELSE
        #END IF/ELIF/ELSE

        #Setting the ReceiverIP based on which IP address was found in the string
        if self.ConnectionLoc == "West":
            __, self.ReceiverIP = EastWestIP
        elif self.ConnectionLoc == "East":
            self.ReceiverIP, __ = EastWestIP
        #END IF/ELIF
    #END DEF

    def __setIperfCommandOpts(self):
        #Checking to make sure that self.iPerfCommand has something in it. Otherwise, exit
        if self.iPerfCommand:
            #Getting port number. Sometimes, this option is not used, so we will default it to 5001
            if "-p" in self.iPerfCommand:
                self.Port = self.iPerfCommand[self.iPerfCommand.find("-p"): ].split(" ")[1].strip()
            else:
                self.Port = "5001"
            #Getting test time interval number
            self.TestInterval = int(self.iPerfCommand[self.iPerfCommand.find("-t"): ].split(" ")[1].strip())
            #Getting measurement format
            self._mform_short = self.iPerfCommand[self.iPerfCommand.find("-f"): ].split(" ")[1].strip()
            if self._mform_short == "k":
                self.MeasuringFmt = ("KBytes","Kbits/sec")
            elif self._mform_short == "K":
                self.MeasuringFmt = ("KBytes","KBytes/sec")
            elif self._mform_short == "m":
                self.MeasuringFmt = ("MBytes","Mbits/sec")
            elif self._mform_short == "M":
                self.MeasuringFmt = ("MBytes","MBytes/sec")
            #END IF/ELIF
        #END IF
    #END DEF

    def __checkForError(self, dataString):
        #Parsing through the big string of text to find error messages for TCP or UDP tests
        if self.ConnectionType in ["TCP","UDP"]:
            if ("Test Timed Out" in dataString) or ("Iperf timed out" in dataString):
                self._ErrorHandling__setErrorCode(121)
            elif ("write1 failed:" in dataString) or ("write2 failed:" in dataString):
                self._ErrorHandling__setErrorCode(102)
            elif "WARNING: did not receive" in dataString:
                self._ErrorHandling__setErrorCode(131)
            elif "[ " not in dataString:
                self._ErrorHandling__setErrorCode(210)
            elif self.ConnectionType is "UDP" and "Server Report" not in dataString:
                self._ErrorHandling__setErrorCode(101)
        #END IF
        if self.ConnectionType == "PING":
            if "Network is unreachable" in dataString:
                self._ErrorHandling__setErrorCode(112)
            elif "Ping timed out" in dataString:
                self._ErrorHandling__setErrorCode(111)
            elif "statistics" not in dataString:
                self._ErrorHandling__setErrorCode(102)
        #END IF
        #Check for all types of tests, if the test was quit by the user
        if ("Quitting operations" in dataString) or ("Quitting Operations" in dataString):
            self._ErrorHandling__setErrorCode(201)
        #END IF
        #Final check for all types of tests, if the test was quit somehow with no other error messages
        if ("bad exit value" in dataString) and not self.ContainsErrors:
            self._ErrorHandling__setErrorCode(103)
        #END IF

        #This is a check for a less possible error. There might be an instance where a test
        # says that it was performing a test connected to the East server, while the IP says that
        # it was connected ot the West server. In this case, the wrong connection was made, the
        # connection location is set to what that "Starting Test" line contains, and self.ContainsErrors
        # is set to True
        if any([(word in dataString) for word in ["East","West"]]):
            if ( ("West" in self.StartingLine) and (self.ConnectionLoc == "East") or
                 ("East" in self.StartingLine) and (self.ConnectionLoc == "West") ):
                #Setting the ConnectionLoc to the expected value, the direction in the test header
                wrongServer = self.ConnectionLoc
                if "West" in self.StartingLine:
                    self.ConnectionLoc = "West"
                elif "East" in self.StartingLine:
                    self.ConnectionLoc = "East"
                #END IF/ELIF
                specialMessage = (
                    "The wrong test was performed for this section. The test should "+
                    "have connected to the "+self.ConnectionLoc+" server, but instead "+
                    "connected to the "+wrongServer+" server."
                )
                self._ErrorHandling__setErrorCode(202, specialMessage)
        #END IF
    #END DEF


    # STRING OUTPUT ------------------------------------------------------------

    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding[:-1] + "-" +
                "Connection Type: {}\n".format(self.ConnectionType) +
                self.StringPadding +
                "Connection Location: {}\n".format(self.ConnectionLoc) +
                self.StringPadding +
                "Receiver: {}:{}\n".format(self.ReceiverIP,self.Port) +
                self.StringPadding +
                "Contain Errors: {}\n".format(repr(self.ContainsErrors)) +
                ((self.StringPadding + "Error Type: " +self.ErrorType+ "\n")
                 if self.ContainsErrors else ""
                 ) +
                ((self.StringPadding + "Error Message: " +self.ErrorMessage+ "\n")
                 if self.ContainsErrors else ""
                 )
                )
    #END DEF
#END CLASS
