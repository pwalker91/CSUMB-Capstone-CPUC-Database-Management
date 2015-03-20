"""
------------------------------------------------------------------------
UDP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual UDP speed test.
            This takes a chunk of text (as a string), and parses out all of the
            header information, like the server connected to, measuring format, etc.
            It then splits the test measurements into their individual threads,
            and passing the resulting strings to the Thread object.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from _Test import Test
from UDP_Thread import UDP_Thread
#END IMPORTS


class UDP_Test(Test):

    """A UDP Test, which is a single upload thread, sending datagrams"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    ConnectionType  = ""
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

    # ---- CLASS ATTRIBUTES ----
    DatagramSize    = 0
    SubTestNumber   = 0
    TargetBandwidth = None  #n[KM]
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
        if "udp" not in dataString.lower():
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (UDP_Test) did not contain "+
                      "the necessary identifiers.",
                      file=sys.stderr)
            return None
        #END IF
        inst = Test.__new__(cls, *args, **kwargs)
        return inst
    #END DEF

    def __init__(self, dataString="", eastWestIP=("0.0.0.0", "0.0.0.0")):
        """
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the raw text that will be parsed
            eastWestIP: Tuple of two Strings, first String is the IP address of the East server, second the West
        """
        #If we are at this point, then the dataString contained "TCP", and we can
        # set the ConnectionType to "TCP"
        self.ConnectionType = "UDP"
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)

        #If we were unable to parse out the iPerfCommand line from the text, then
        # we assume that there was an error of some kind that was not caught, and exit
        if not self.iPerfCommand:
            self._ErrorHandling__setErrorCode(101, "Iperf Command Line not Found")
            #raise RuntimeError("For some reason, the Iperf command line was not parsed.")
        else:
            #Getting the datagram size
            self.DatagramSize = self.iPerfCommand[self.iPerfCommand.find("-l"):].split(" ")[1].strip()
            #Getting the datagram size
            self.TargetBandwidth = self.iPerfCommand[self.iPerfCommand.find("-b"):].split(" ")[1].strip()
            self.SubTestNumber = 0
            if not self.ContainsErrors:
                #Declaring and creating the UDP Thread for this test
                self.Threads = []
                dataArray = [line for line in self._text if ("[ " in line)]
                threadNum = int(dataArray[0].split("]")[0].split("[")[1].strip())
                self.Threads.append( UDP_Thread(dataArr=dataArray,
                                                threadNum=threadNum,
                                                direction="UP",
                                                units=self.MeasuringFmt) )
            #END IF
        #END IF/ELSE
    #END DEF


# STRING OUTPUT ----------------------------------------------------------------

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (  self.StringPadding[:-1] + "-" +
                    "Test Number: {}\n".format(self.TestNumber) +
                    ((self.StringPadding +
                      "Sub Test Number: {}\n".format(self.SubTestNumber))
                     if (self.SubTestNumber != 0) else ""
                     ) +
                    self.StringPadding +
                    "Connection Type: {}\n".format(self.ConnectionType) +
                    self.StringPadding +
                    "Connection Location: {}\n".format(self.ConnectionLoc) +
                    self.StringPadding +
                    "Receiver IP: {}:{}\n".format(self.ReceiverIP,self.Port) +
                    self.StringPadding +
                    "Test Interval: {}".format(self.TestInterval) +
                    "  Datagram Size: {}\n".format(self.DatagramSize) +
                    self.StringPadding +
                    "Target Bandwidth: {}".format(self.TargetBandwidth) +
                    "  Measurement Format: {}, {}\n".format(self.MeasuringFmt[0],
                                                            self.MeasuringFmt[1]) +
                    self.StringPadding +
                    "Contain Errors: {}\n".format(repr(self.ContainsErrors)) +
                    ((self.StringPadding + "Error Type: " +self.ErrorType+ "\n")
                     if self.ContainsErrors else ""
                     ) +
                    ((self.StringPadding + "Error Message: " +self.ErrorMessage+ "\n")
                     if self.ContainsErrors else ""
                     )
                    )
        if not self.ContainsErrors:
            for thread in self.Threads:
                string += str(thread)
        #END IF
        return string
    #END DEF
#END CLASS
