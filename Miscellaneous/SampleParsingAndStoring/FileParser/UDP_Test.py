"""
------------------------------------------------------------------------
UDP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual UDP speed test.
            This takes a chunk of text (as a string), and parses out all of the header information,
            like the server connected to, measuring format, etc. It then splits the test measurements
            into their individual threads, and passing the resulting strings to the Thread object.

FUNCTIONS:
    __init__
    get_csvDefaultValues
    __str__
------------------------------------------------------------------------
"""


# IMPORTS
from _Test import Test
from UDP_Thread import UDP_Thread
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


    def __init__(self, dataString="", eastWest=("0.0.0.0", "0.0.0.0")):
        """
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the raw text that will be parsed
            eastWest:   Tuple of two Strings, first String is the IP address of the East server, second the West
        """
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
    #END DEF

    def get_csvDefaultValues(self):
        """
        Returns a List of the default CSV values needed for the creation of a CSV
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
        RETURNS:
            List, the values necessary for the creation of the CSV file
        """
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

    def __str__(self):
        """Returns a string represenation of the object"""
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
