"""
------------------------------------------------------------------------
_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class is the bare bones for the TCP, UDP, and PING Test classes, as all test have different
            formats for their information, and different things that we want to track

VARIABLES:    The variables below are possibly common to TCP, UDP, PING, and TCRT tests
    ConnectionType      String, represents the type of connection (TCP, UDP, PING, or TCRT)
    ConnectionLoc       String, represents where this test is connected to (East or West)
    Threads             List, holding all of the PingThreads in this test
    TestNumber          Integer, the number of this test (order in which it was run)
    ReceiverIP          String, IP of the server this test is connected to
    Port                Integer, the port this test is connected to
    TestInterval        Integer, the length of time that the test will be run
    MeasuringFmt        String, the format (Kbytes, Kbits, etc.) that the data has been stored in
    _mform_short        String, usual only one character. The character used when iPerf was run to
                            choose the measuring format
    _text               List of Strings, the raw data, split by '\n'
    iPerfCommand        String, the command line string used to run iPerf for this test
    StartingLine        String, the first line of text in this whole test

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
                    dataString: String, the raw text that will be parsed
                    eastWest:   Tuple of two Strings, first String is IP address of  East server, second is West
                    short:      Boolean, determines detail of printout in __str__
        OUTPUTS-    none
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
  ------------------------------------------------------------------------
"""


# IMPORTS
#Import some global vars from data_utils
from PyObjects.__Base import (Formatting, ErrorHandling)
#END IMPORTS

# CLASS
class Test(Formatting, ErrorHandling):
    # ------------------------------
    # Class attributes
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


    # DESC: Initializing class
    def __init__(self, dataString="", eastWest=("0.0.0.0", "0.0.0.0")):
        #Inheritting our formatting and error handling
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding * 2
        ErrorHandling.__init__(self)
        #Actual initialization
        self._text = dataString.split('\n')
        #This removes all lines that contain nothing
        self._text = [line for line in self._text if line]

        #Determining whether the test is a UDP, TCP, or PING
        if "TCP" in dataString:
            self.ConnectionType = "TCP"
        elif "UDP" in dataString:
            self.ConnectionType = "UDP"
        elif any( [(string in dataString) for string in ["ping", "Ping"]] ):
            self.ConnectionType = "PING"
        elif any( [(string in dataString) for string in ["traceroute", "Traceroute"]] ):
            self.ConnectionType = "TCRT"
        #END IF/ELIFx2

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

        #Determining the Connection Location
        eastIP, westIP = eastWest
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
            __, self.ReceiverIP = eastWest
        elif self.ConnectionLoc == "East":
            self.ReceiverIP, __ = eastWest
        #END IF/ELIF

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

        #Parsing through the big string of text to find error messages for TCP or UDP tests
        if self.ConnectionType in ["TCP","UDP"]:
            if ("Test Timed Out" in dataString) or ("Iperf timed out" in dataString):
                self.ContainsErrors = True
                self.ErrorCode = 121
                return
            elif ("write1 failed:" in dataString) or ("write2 failed:" in dataString):
                self.ContainsErrors = True
                self.ErrorCode = 102
                return
            elif "WARNING: did not receive" in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 131
                return
            elif "[ " not in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 210
                return
            elif self.ConnectionType is "UDP" and "Server Report" not in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 101
                return
        #END IF
        if self.ConnectionType == "PING":
            if "Network is unreachable" in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 112
                return
            elif "Ping timed out" in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 111
                return
            elif "statistics" not in dataString:
                self.ContainsErrors = True
                self.ErrorCode = 102
                return
        #END IF
        #Check for all types of tests, if the test was quit by the user
        if ("Quitting operations" in dataString) or ("Quitting Operations" in dataString):
            self.ContainsErrors = True
            self.ErrorCode = 201
            return
        #END IF
        #Final check for all types of tests, if the test was quit somehow with no other error messages
        if ("bad exit value" in dataString) and (self.ContainsErrors == False):
            self.ContainsErrors = True
            self.ErrorCode = 103
            return
        #END IF
        #This is a check for a less possible error. There might be an instance where a test
        # says that it was performing a test connected to the East server, while the IP says that
        # it was connected ot the West server. In this case, the wrong connection was made, the
        # connection location is set to what that "Starting Test" line contains, and self.ContainsErrors
        # is set to True
        if any([(word in dataString) for word in ["East","West"]]):
            if ( ("West" in self.StartingLine) and (self.ConnectionLoc == "East")  or
                 ("East" in self.StartingLine) and (self.ConnectionLoc == "West") ):
                #Setting the ConnectionLoc to the expected value, the direction in the test header
                wrongServer = self.ConnectionLoc
                if "West" in self.StartingLine:
                    self.ConnectionLoc = "West"
                elif "East" in self.StartingLine:
                    self.ConnectionLoc = "East"
                #END IF/ELIF
                self.ContainsErrors = True
                self.ErrorCode = 202
                self.ErrorMessages[self.ErrorCode] = (
                        "The wrong test was performed for this section. The test should "+
                        "have connected to the "+self.ConnectionLoc+" server, but instead "+
                        "connected to the "+wrongServer+" server." )
                return
        #END IF
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (self.StringPadding +
                    "Connection Type: " + self.ConnectionType + "\n" +
                self.StringPadding +
                    "Connection Location: " + self.ConnectionLoc + "\n" +
                self.StringPadding +
                    "Receiver: " + self.ReceiverIP + ":" + self.Port + "\n" +
                self.StringPadding +
                    "Contain Errors: " + repr(self.ContainsErrors) + "\n" +
                    ((self.StringPadding +
                        "Error Type: " +self.ErrorTypes[self.ErrorCode]+ "\n") \
                      if self.ContainsErrors else "" ) +
                    ((self.StringPadding +
                        "Error Message: " +self.ErrorMessages[self.ErrorCode]+ "\n") \
                      if self.ContainsErrors else "" )
                )
    #END DEF
#END CLASS