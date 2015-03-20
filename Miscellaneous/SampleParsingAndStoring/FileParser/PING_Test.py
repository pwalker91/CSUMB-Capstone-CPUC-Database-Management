"""
------------------------------------------------------------------------
PING_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual Ping test. This class keeps track of the RTT values for each
            ping, and the final ping statistics.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from parserUtils.basic_utils import calc_rVal_MOS
from _Test import Test
from __Base import Formatting
#END IMPORTS




class PING_Packet(Formatting):

    """A simple class for holding the information from a single PING packet"""

    '''
    # ------------------------------
    # ---- CLASS VARIABLES ----
    RTT = -1
    TTL = 0
    # ------------------------------
    '''

    def __init__(self, dataString, _outputType1=True):
        """Object initialization"""
        #Inheritting our formatting
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding * 3
        #Setting an array of strings that are key strings we are looking for.
        # If any are found, then there was an error in the test, and we set our
        # object attributes to default values
        possiblePingErrors = ["request timed out",
                              "request timeout",
                              "general failure",
                              "no resources",
                              "host unreachable",
                              "net unreachable",
                              "dest unreachable",
                              "time to live exceeded" ]
        if any([error in dataString.lower() for error in possiblePingErrors]):
            self.RTT = -1
            self.TTL = 0
        else:
            self.RTT = float(dataString.lower().split("time=")[-1]
                                               .split(" ")[0]
                                               .split("ms")[0]
                                               .strip()
                             )
            self.TTL = float(dataString.lower().split("ttl=")[-1]
                                               .split(" ")[0]
                                               .strip()
                             )
        #END IF/ELSE
    #END DEF

    def __str__(self):
        """Returning a string representation of the object"""
        return (self.StringPadding +
                "RTT={}ms  TTL={}".format(self.RTT, self.TTL))
    #END DEF
#END CLASS





class PING_Test(Test):

    """A PING test, containing parsed information about ping packets sent"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    ConnectionType  = ""
    ConnectionLoc   = ""
    TestNumber      = 0
    ReceiverIP      = ""
    StartingLine    = ""
    _text           = ""

    # ---- CLASS ATTRIBUTES ----
    Times           = None
    PacketsSent     = 10
    PacketsReceived = 0
    PacketsLost     = 10

    RTTMin          = -1
    RTTMax          = -1
    RTTAverage      = -1
    is_outputType1  = True
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
        if "ping" not in dataString.lower():
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (PING_Test) did not contain "+
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
            dataString: String, the text that is going to be parsed
            eastWestIP: Tuple of two Strings, first String is the IP address of the East server, second the West
        """
        #If we are at this point, then the dataString contained "ping", and we can
        # set the ConnectionType to "PING"
        self.ConnectionType = "PING"
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)
        self.Times = []

        #A quick check that we do not have weird formatting of our PING test.
        # Sometimes, there are cases where there are two newline characters between
        # each line of data.
        if "\n\n\n" in dataString:
            self._ErrorHandling__setErrorCode(101)
        #Now we parse out the Pings from the test
        if not self.ContainsErrors:
            #We need to first figure out if the test is from a mobile device,
            # or netbook (for Field Test files). This also differentiates between Phone
            # and Desktop in Crowd Source files.
            if "Ping statistics for" not in dataString:
                self.is_outputType1 = True
            else:
                self.is_outputType1 = False
            #END IF/ELSE
            self.parsePings(dataString)
        else:
            self.PacketsSent     = 10
            self.PacketsReceived = 0
            self.PacketsLost     = 10
            self.RTTMin          = -1
            self.RTTMax          = -1
            self.RTTAverage      = -1
        #END IF/ELSE
        if len(self.Times) != self.PacketsSent:
            self.PacketsSent = len(self.Times)
    #END DEF


# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def parsePings(self, dataString):
        """ Parses out all of the Ping test information (individual ping RTTs and total RTT stats)"""
        #We start our function be splitting the data string into individual chunks,
        # which we will then parse individually
        dataChunks = [elem.strip() for elem in dataString.split("\n\n") if elem]
        statsText = "ping statistics" if self.is_outputType1 else "Ping statistics"
        for chunk in dataChunks:
            if statsText in chunk:
                self.__parseStats(chunk)
            #If the string 'bytes of data' is in the chunk, then we are looking
            # at the chunk holding all of the ping packet results
            if "bytes of data" in chunk:
                self.__parseIndividualPings(chunk, "bytes of data")
            elif "data bytes" in chunk:
                self.__parseIndividualPings(chunk, "data bytes")
        #END FOR
    #END DEF

    def __parseIndividualPings(self, dataString, splitter):
        #As we know that we are looking at the chunk of data that is the ping
        # packet RTTs, we want to first get some basic information. All that
        # we can really glean is the packet size in bytes
        allData = dataString.split(splitter)[-1].split("\n")
        #This list comprehension removes all strings that are only a few characters.
        # Each packet should have caused a message longer than 5 characters to be printed
        allData = [elem for elem in allData if len(elem)>5]
        #Now we want to remove any strings that are a redirect message
        allData = [elem for elem in allData if "redirect host" not in elem.lower()]
        for packet in allData:
            self.Times.append(PING_Packet(packet, self.is_outputType1))
    #END DEF

    def __parseStats(self, dataString):
        #Depending on whether our ouput was of one type or another, we will follow
        # different rules for parsing
        dataString = dataString.split("\n")
        if self.is_outputType1:
            #First declare packetsLine to be the first element, and then split it by ",".
            # Then parse the packets sent and received, and deduce the packets lost
            packetsLine = dataString[1]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = int(packetsLine[0].split(" ")[0])
            self.PacketsReceived = int(packetsLine[1].strip().split(" ")[0])
            self.PacketsLost = int(self.PacketsSent - self.PacketsReceived)
            #This try/except block is needed, as sometimes the min/avg/max numbers
            # are not printed out by iPerf. This happens in the case of 100% packet loss
            try:
                RTTLine = dataString[2]
                RTTNums = RTTLine.split("=")[1].strip().split("/")
                self.RTTMin = float(RTTNums[0])
                self.RTTAverage = float(RTTNums[1])
                self.RTTMax = float(RTTNums[2])
            except:
                self.RTTMin     = -1
                self.RTTMax     = -1
                self.RTTAverage = -1
        else:
            #First declare packetsLine to be the first element, and then split it by ",".
            # Then parse the packets sent and lost
            packetsLine = dataString[1]
            packetsLine = packetsLine.split(",")
            self.PacketsSent = int(packetsLine[0].split("=")[1].strip())
            self.PacketsReceived = int(packetsLine[1].split("=")[1].strip())
            self.PacketsLost = int(packetsLine[2].split("=")[1].strip().split(" ")[0])
            #This try/except block is needed, as sometimes the min/avg/max numbers
            # are not printed out by iPerf. This happens in the case of 100% packet loss
            try:
                RTTLine = dataString[3]
                RTTLine = RTTLine.split(",")
                self.RTTMin = float(RTTLine[0].split("=")[1][:-2].strip())
                self.RTTMax = float(RTTLine[1].split("=")[1][:-2].strip())
                self.RTTAverage = float(RTTLine[2].split("=")[1][:-2].strip())
            except:
                self.RTTMin     = -1
                self.RTTMax     = -1
                self.RTTAverage = -1
        #END IF/ELSE
    #END DEF


# CALCULATIONS -----------------------------------------------------------------

    def calc_rValMOS(self, delayThreshold=150):
        """
        Calculates the R-Value and MOS score for this connection based on the RTT
        values recorded in the test.
        """
        if not self.ContainsErrors:
            #Setting the variables which will hold the float values passed to the
            # original calc_rVal_MOS function
            totalCnt = 0.0
            totalLost = 0.0
            totalTPng = float(len(self.Times))
            totalSum = 0.0
            totalMax = 0.0
            # F(d) -the rate of packets below delay threshold, done by incrementing
            # this value for every packet that is below delayThreshold and then dividing by
            # the total number of measurements. This value is recorded in the variable below
            totalFd = 0.0
            #We will now begin to calculate the values that will be passed to the
            # original calculation function
            totalMax = self.RTTMax if (totalMax < self.RTTMax) else totalMax
            totalLost += self.PacketsLost
            #Now we loop through all of the ping times so that we can add them to the
            # totalSum variable. If the time retrieved is not 0, the value is added
            # to the totalSum variable and totalCnt is incremented. We also increment
            # "Fd" if the time is above the given threshold "delayThreshold"
            for pingPacket in self.Times:
                if pingPacket.RTT > 0:
                    totalCnt += 1
                    totalSum += pingPacket.RTT
                    if (pingPacket.RTT < delayThreshold):
                        totalFd+=1
                    #END IF
                #END IF
            #END FOR
            #Returning (rVal, MOS)
            if totalCnt != 0:
                return calc_rVal_MOS(totalSum, totalCnt, totalTPng, totalLost, totalFd)
            else:
                return [0.0,1.0]
        else:
            return [self.ErrorType]*2
    #END DEF


# GETTERS ----------------------------------------------------------------------

    def get_TimesAsArray(self):
        """Returns a list of the Times values, for more simple use by other scripts"""
        return [self.Times[ind].RTT for ind in range(len(self.Times))]
    #END DEF


# STRING PRINTOUT --------------------------------------------------------------

    def __str__(self):
        """Returns a string representation of the object"""
        string = (self.StringPadding[:-1] + "-" +
                  "Test Number: {}\n".format(self.TestNumber) +
                  self.StringPadding +
                  "Connection Type: {}\n".format(self.ConnectionType) +
                  self.StringPadding +
                  "Connection Location: {}\n".format(self.ConnectionLoc) +
                  self.StringPadding +
                  "Receiver IP: {}\n".format(self.ReceiverIP) +
                  self.StringPadding +
                  "Contain Errors: {}\n".format(repr(self.ContainsErrors)) +
                  ((self.StringPadding +"Error Type: "+self.ErrorType+"\n")
                   if self.ContainsErrors else ""
                   ) +
                  ((self.StringPadding +"Error Message: "+self.ErrorMessage+"\n")
                   if self.ContainsErrors else ""
                   )
                  )
        if not self.ContainsErrors:
            #Printing the individual pings in the ping test
            pingTimes = self.StringPadding + "  Ping Times: "
            #Putting all of the times into a string. If there were more than 7, then
            # will will print all of the pings onto two lines. Else, all on one
            if len(self.Times) > 7:
                length = len(self.Times)
                for i in range(int(length/2)):
                    pingTimes += "{}={}ms, ".format(i+1, self.Times[i].RTT)
                #This bit takes the ', ' off of the end, tacks on a newline, and then
                # the necessary number of spaces to line it up with the first row of Ping times
                pingTimes = pingTimes[:-2]+"\n"+self.StringPadding+(" "*(len("  Ping Times: ")))
                for i in range(int(length/2), length):
                    pingTimes += "{}={}ms, ".format(i+1, self.Times[i].RTT)
            else:
                for i in range(len(self.Times)):
                    pingTimes += "{}={}ms, ".format(i+1, self.Times[i].RTT)
            #END IF/ELSE
            string += pingTimes[:-2]+"\n"
            #Printing the rest of the information
            string += (self.StringPadding +
                       "  Packets Sent: {}\n".format(self.PacketsSent) +
                       self.StringPadding +
                       "  Packets Received: {}\n".format(self.PacketsReceived) +
                       self.StringPadding +
                       "  Packets Lost: {}\n".format(self.PacketsLost) +
                       self.StringPadding +
                       "  Round Trip Time Minimum: {}\n".format(self.RTTMin) +
                       self.StringPadding +
                       "  Round Trip Time Maximum: {}\n".format(self.RTTMax) +
                       self.StringPadding +
                       "  Round Trip Time Average: {}\n".format(self.RTTAverage)
                       )
        #END IF
        return string
    #END DEF
#END CLASS
