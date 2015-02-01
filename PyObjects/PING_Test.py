"""
------------------------------------------------------------------------
PING_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual Ping test. This class keeps track of the RTT values for each
            ping, and the final ping statistics.

VARIABLES:
  INHERITED
    ConnectionType      String, represents the type of connection (TCP, UDP, or PING)
    ConnectionLoc       String, represents where this test is connected to (East or West)
    TestNumber          Integer, the number of this test (order in which it was run)
    ReceiverIP          String, IP of the server this test is connected to
    StartingLine        String, the first line of text in this whole test
    _text               List of Strings, the raw data, split by '\n'
  NOT INHERITED
    Times               List, holds all of the individual ping times in the test
    PacketsSent         Integer, number of packets sent during the test
    PacketsReceived     Integer, number of packets received by the host
    PacketsLost         Integer, number of packets not received by the recipient
    RTTMin              Integer, RTT min recorded by the test
    RTTMax              Integer, RTT max recorded by the test
    RTTAverage          Integer, RTT average recorded by the test
    is_outputType1      Boolean, if the test was on a mobile device, the format is different

FUNCTIONS:
  INITIALIZATION
    __init__ - Used to initialize an object of this class
        INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
                    dataString:     String, the text that is going to be parsed
                    isMobile:       Boolean, whether this test was taken on a mobile or netbook device
                    short:          Boolean, whether to print this object in short or long form
        OUTPUTS-    none
    parsePings - Parses out all of the Ping test information (individual ping RTTs and total RTT stats)
                from the text stored in self._text
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    none

  CALCULATIONS
    calc_rValMOS - Calculates the R-Value and MOS score for this connection based on the
                RTT values recorded in the test.
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the R-value and MOS score for this PING test

  GETTER
    get_TimesAsArray - Returns a list of the Times values, for more simple use by other scripts
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values in self.Times in sequence
    get_csvDefaultValues - Returns a List of the default CSV values needed for the creation of a CSV
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values necessary for the creation of the CSV file
    get_csvRvMosValues - Returns a List of the R-value and MOS Score values
                needed for the creation of a CSV
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values necessary for the creation of the CSV file

  STRING PRINOUT
    __str__ - Returns a string representation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
------------------------------------------------------------------------
"""


# IMPORTS
from PyObjects.utils.basic_utils import calc_rVal_MOS
from PyObjects._Test import Test
#END IMPORTS

# CLASS
class PING_Test(Test):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ConnectionType  = ""
    # ConnectionLoc   = ""
    # TestNumber      = 0
    # ReceiverIP      = ""
    # StartingLine    = ""
    # _text           = ""

    # Class attributes
    Times           = None
    PacketsSent     = 10
    PacketsReceived = 0
    PacketsLost     = 10

    RTTMin          = -1
    RTTMax          = -1
    RTTAverage      = -1
    is_outputType1  = True
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString="", eastWest=("0.0.0.0", "0.0.0.0")):
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWest=eastWest)
        self.Times = {}
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
            self.parsePings()
        #END IF
        #Clearing the values in self._text so we don't waste some space
        self._text = None
    #END DEF


# Intialization Functions ----------------------------------------------------------------

    # DESC: Parses out all of the Ping test information (individual ping RTTs and total RTT stats) from the text
    def parsePings(self):
        #Getting the Receiver IP address
        statsStartHere = -1
        pingCounter = 0
        statsText = "ping statistics" if self.is_outputType1 else "Ping statistics"
        pingText = "bytes from" if self.is_outputType1 else "Reply from"
        possiblePingErrors = ["Request timed out", "General failure",
                              "host unreachable", "net unreachable" ]
        #One quick check to make sure that there are pings to parse. If not, then
        # we create a bunch of 0's in self.Times
        stuffToParse = False
        for line in self._text:
            if pingText in line: stuffToParse = True
        #END FOR
        #If there is nothing to parse, then we create a test of no pings
        if not stuffToParse:
            for ind in range(1,11):
                self.Times[ind] = float(0)
        #END IF

        #Now we loop through all of the text until we have parsed all of the pings and
        # have found the statistics line
        for line in self._text:
            #This test comes first so that, when we reach the statistics at the bottom, we read it,
            # parse it, and then break out of the loop before the other conditional are run
            if statsText in line:
                statsStartHere = self._text.index(line)
                break
            #Parse the individual ping times from the test
            else:
                #This checks to see if there are any error messages in the ping message. If there
                # was an error, the boolean isErrorPresent is made true, and the loop does not continue to
                # "if pingText in line", as the line will not have the information we need, and the .split()
                # will break. A time of 0 is inserted into self.Times as a placeholder.
                if any( [(error in line) for error in possiblePingErrors] ):
                    pingCounter += 1
                    self.Times[pingCounter] = float(0)
                    continue
                #END FOR
                if pingText in line:
                    pingCounter += 1
                    self.Times[pingCounter] = float(line.split("time=")[1].split("ms")[0].strip())
                #END IF
            #END IF/ELSE
        #END FOR
        #This is a last check to make sure that our self.Times dictionary has placeholders
        # for all of the packets. In CrowdSource Files, missing pings seem to not print anything
        for ind in range(1,11):
            try:
                __ = self.Times[ind]
            except KeyError:
                self.Times[ind] = float(0)
            #END TRY/EXCEPT
        #END FOR

        #If the variable statsStartHere is not changed from -1, then we can assume that
        # the necessary line was never found. If it has changed, then we can parse the statistics
        if statsStartHere != -1:
            statsArr = self._text[statsStartHere:]
            if self.is_outputType1:
                #First declare packetsLine to be the first element, and then split it by ",".
                # Then parse the packets sent and received, and deduce the packets lost
                packetsLine = statsArr[1]
                packetsLine = packetsLine.split(",")
                self.PacketsSent = int(packetsLine[0].split(" ")[0])
                self.PacketsReceived = int(packetsLine[1].strip().split(" ")[0])
                self.PacketsLost = int(self.PacketsSent - self.PacketsReceived)
                #This try/except block is needed, as sometimes the min/avg/max numbers
                # are not printed out by iPerf. This happens in the case of 100% packet loss
                try:
                    RTTLine = statsArr[2]
                    RTTNums = RTTLine.split("=")[1].strip().split("/")
                    self.RTTMin = float(RTTNums[0])
                    self.RTTAverage = float(RTTNums[1])
                    self.RTTMax = float(RTTNums[2])
                except:
                    using_defaults_of_0 = True
            else:
                #First declare packetsLine to be the first element, and then split it by ",".
                # Then parse the packets sent and lost
                packetsLine = statsArr[1]
                packetsLine = packetsLine.split(",")
                self.PacketsSent = int(packetsLine[0].split("=")[1].strip())
                self.PacketsReceived = int(packetsLine[1].split("=")[1].strip())
                self.PacketsLost = int(packetsLine[2].split("=")[1].strip().split(" ")[0])
                #This try/except block is needed, as sometimes the min/avg/max numbers
                # are not printed out by iPerf. This happens in the case of 100% packet loss
                try:
                    RTTLine = statsArr[3]
                    RTTLine = RTTLine.split(",")
                    self.RTTMin = float(RTTLine[0].split("=")[1][:-2].strip())
                    self.RTTMax = float(RTTLine[1].split("=")[1][:-2].strip())
                    self.RTTAverage = float(RTTLine[2].split("=")[1][:-2].strip())
                except:
                    using_defaults_of_0 = True
            #END IF/ELSE
        #END IF
    #END DEF


# Calculations ---------------------------------------------------------------------------

    # DESC: Calculates the R-value and MOS score of this connection based on the RTT
    #       times in this PING Test
    def calc_rValMOS(self, delayThreshold=150):
        #Setting the variables which will hold the float values passed to the
        # original calc_rVal_MOS function
        totalCnt = 0.0; totalLost = 0.0
        totalTPng = float(len(self.Times))
        totalSum = 0.0; totalMax = 0.0
        # F(d) -the rate of packets below delay threshold, done by incrementing
        # this value for every packet that is below delayThreshold and then dividing by
        # the total number of measurements. This value is recorded in the variable below
        totalFd = 0.0
        if not self.ContainsErrors:
            #We will now begin to calculate the values that will be passed to the
            # original calculation function
            totalMax = self.RTTMax if (totalMax < self.RTTMax) else totalMax
            totalLost += self.PacketsLost
            #Now we loop through all of the ping times so that we can add them to the
            # totalSum variable. If the time retrieved is not 0, the value is added
            # to the totalSum variable and totalCnt is incremented. We also increment
            # "Fd" if the time is above the given threshold "delayThreshold"
            for index in self.Times:
                time = self.Times[index]
                if time > 0:
                    totalCnt += 1; totalSum += time
                    if (time < delayThreshold):
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
            return [self.ErrorTypes[self.ErrorCode]]*2
    #END DEF


# Getter - Times as array of nums --------------------------------------------------------

    # DESC: Returns the times stored in this object Times attribute as an array of numbers
    def get_TimesAsArray(self):
        return [self.Times[ind] for ind in range(0,len(self.Times))]
    #END DEF

    # DESC: Returns an array of the necessary values for the CSV file being created
    def get_csvDefaultValues(self):
        csvVals = []
        if not self.ContainsErrors:
            csvVals.append(self.RTTMin)
            csvVals.append(self.RTTMax)
            csvVals.append(self.RTTAverage)
            LossPercent = int(float(self.PacketsLost)*100/self.PacketsSent)
            csvVals.append(LossPercent)
        else:
            csvVals = [self.ErrorTypes[self.ErrorCode]]*4
        return csvVals
    #END DEF

    # DESC: Returns an array of the necessary values for the CSV file being created
    def get_csvRvMosValues(self):
        return self.calc_rValMOS()
    #END DEF


# String printout -------------------------------------------------------------------------

    # DESC: Creating a string representation of our object
    def __str__(self):
        string = (self.StringPadding +
                        "Test Number: " + str(self.TestNumber) + "\n" +
                  self.StringPadding +
                        "Connection Type: " + str(self.ConnectionType) + "\n" +
                  self.StringPadding +
                        "Connection Location: " + str(self.ConnectionLoc) + "\n" +
                  self.StringPadding +
                        "Receiver IP: " + str(self.ReceiverIP) + "\n" +
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
            #Printing the individual pings in the ping test
            pingTimes = self.StringPadding + "  Ping Times: "
            #Getting some information on where to split the string later
            beginningLen = len(pingTimes)
            #Printing out all of the times
            for index in self.Times:
                pingTimes += (str(index) + "=" + str(self.Times[index]) + "ms, ")
            #Splitting the string in the middle of the pings only if there are more that 7
            if len(self.Times) > 7:
                timesKeys = list(self.Times.keys()); timesKeys.sort()
                middleInd = timesKeys[int(len(timesKeys)/2)]
                locOfMid = pingTimes.index( (str(middleInd)+"=") )
                pingTimes = pingTimes[:locOfMid] + "\n"+(" "*beginningLen) + pingTimes[locOfMid:-2] + "\n"
            #END IF
            string += pingTimes
            #Printing the rest of the information
            string += (self.StringPadding +
                        "  Packets Sent: " + str(self.PacketsSent) + "\n" +
                       self.StringPadding +
                        "  Packets Received: " + str(self.PacketsReceived) + "\n" +
                       self.StringPadding +
                        "  Packets Lost: " + str(self.PacketsLost) + "\n" +
                       self.StringPadding +
                        "  Round Trip Time Minimum: " + str(self.RTTMin) + "\n" +
                       self.StringPadding +
                        "  Round Trip Time Maximum: " + str(self.RTTMax) + "\n" +
                       self.StringPadding +
                        "  Round Trip Time Average: " + str(self.RTTAverage) + "\n"
                      )
        #END IF
        return string
    #END DEF
#END CLASS
