"""
------------------------------------------------------------------------
UDP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual UDP speed test.
            This takes a chunk of text (as a string), and parses out all of the header information,
            like the server connected to, measuring format, etc. It then splits the test measurements
            into their individual threads, and passing the resulting strings to the Thread object.

VARIABLES:
  INHERITED
    ConnectionType      String, represents the type of connection (TCP, UDP, or PING)
    ConnectionLoc       String, represents where this test is connected to (East or West)
    Threads             List, holding all of the TCP_Threads in this test, accessed by [direction][index]
                            note: index is NOT the thread number
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
  NOT INHERITED
    SubTestNumber       Integer, if the UDP test is one of three 1 second UDP test in a Field test, this
                            will hold which number this test was in that order.
    DatagramSize        The size of datagrams that will be sent
    TargetBandwidth     String, the targetted bandwidth to be used in this test

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:       reference to the object calling this method (i.e. Java's THIS)
                    dataString: String, the raw text that will be parsed
                    eastWest:   Tuple of two Strings, first String is the IP address of the East server, second the West
                    short:      Boolean, determines detail of printout in __str__
        OUTPUTS-    none
    get_csvDefaultValues - Returns a List of the default CSV values needed for the creation of a CSV
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values necessary for the creation of the CSV file
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
------------------------------------------------------------------------
"""


# IMPORTS
from PyObjects._Test import Test
from PyObjects.UDP_Thread import UDP_Thread
#END IMPORTS

class UDP_Test(Test):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ConnectionType  = ""
    # ConnectionLoc   = ""
    # Threads         = None
    # TestNumber      = 0
    # ReceiverIP      = ""
    # Port            = 0000
    # TestInterval    = 0
    # MeasuringFmt    = None  #[kmKM] (Kbits, Mbits, KBytes, MBytes)
    # _mform_short    = None
    # _text           = ""
    # iPerfCommand    = ""
    # StartingLine    = ""

    # Class variables
    DatagramSize    = 0
    SubTestNumber   = 0
    TargetBandwidth = None  #n[KM]
    # ------------------------------


    # DESC: Initializing class
    def __init__(self, dataString="", eastWest=("0.0.0.0", "0.0.0.0")):
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWest=eastWest)
        if not self.iPerfCommand: return
        #Getting the datagram size
        self.DatagramSize = self.iPerfCommand[self.iPerfCommand.find("-l"):].split(" ")[1].strip()
        #Getting the datagram size
        self.TargetBandwidth = self.iPerfCommand[self.iPerfCommand.find("-b"):].split(" ")[1].strip()
        if not self.ContainsErrors:
            #Declaring and creating the UDP Thread for this test
            self.Threads = []
            dataArray = [line for line in self._text if ("[ " in line)]
            threadNum = int(dataArray[0].split("]")[0].split("[")[1].strip())
            self.Threads.append( UDP_Thread(dataArr=dataArray, threadNum=threadNum, direction="UP",
                                            units=self.MeasuringFmt) )
        #END IF
        #Clearing the values in self._text so we don't waste some space
        self._text = None
    #END DEF

    # DESC: Creates a List of the test's Jitter, datagram loss percentage, and test interval time
    def get_csvDefaultValues(self):
        csvVals = []
        if not self.ContainsErrors:
            csvVals.append(self.Threads[0].ServerReport.Jitter)
            csvVals.append(self.Threads[0].ServerReport.Dtgrams_Perc)
        else:
            csvVals = [self.ErrorTypes[self.ErrorCode]]*2
        #END IF/ELSE
        csvVals.append(self.TestInterval)
        return csvVals
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        string = (  self.StringPadding +
                        "Test Number: " + str(self.TestNumber) + "\n" +
                    ((self.StringPadding +
                        "Sub Test Number: "+str(self.SubTestNumber)+"\n") \
                      if (self.SubTestNumber != 0) else "") +
                    self.StringPadding +
                        "Connection Type: " + str(self.ConnectionType) + "\n" +
                    self.StringPadding +
                        "Connection Location: " + str(self.ConnectionLoc) + "\n" +
                    self.StringPadding +
                        "Receiver IP: " + str(self.ReceiverIP) + ":" + str(self.Port) + "\n" +
                    self.StringPadding +
                        "Test Interval: " + str(self.TestInterval) +
                        "  Datagram Size: " + str(self.DatagramSize) + "\n" +
                    self.StringPadding +
                        "Target Bandwidth: " + str(self.TargetBandwidth) +
                        "  Measurement Format: " + str(self.MeasuringFmt[0]) +
                                             ", " + str(self.MeasuringFmt[1]) + "\n" +
                    self.StringPadding +
                        "Contain Errors: " + repr(self.ContainsErrors) + "\n" +
                        ((self.StringPadding + \
                            "Error Type: " + self.ErrorTypes[self.ErrorCode] + "\n") \
                          if self.ContainsErrors else "" ) +
                        ((self.StringPadding + \
                            "Error Message: " + self.ErrorMessages[self.ErrorCode] + "\n") \
                          if self.ContainsErrors else "" )
                  )
        if not self.ContainsErrors:
            for thread in self.Threads:
                string += str(thread)
        #END IF
        return string
    #END DEF
#END CLASS
