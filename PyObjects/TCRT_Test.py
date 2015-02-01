"""
------------------------------------------------------------------------
TCRT_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual trace route test. This class keeps track of the
            RTT values for each step along the route, as well as information on the hop. This
            class uses a sub-class included in this file, the Hop class.

------------------------------------------------------------------------
"""

# IMPORTS
from PyObjects.__Base import (Formatting, ErrorHandling)
#END IMPORTS









"""
------------------------------------------------------------------------
HOP Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual hop within the traceroute. This object
            essentially represents one line in the test

VARIABLES:
    HopNum      Integer, the number hop this was in the string of hops on the traceroute
    RTT         Float, the time in milliseconds for a message to get to the router and back
    RouterName  String, the name of the router this information is coming from
    RouterIP    String, the IP address of the router this info is coming from
    _Timeout    Boolean, whether this hop timed out or not
    _short_str_method   Boolean, whether the object prints long or short version on __str__
------------------------------------------------------------------------
"""

# CLASS
class Hop(Formatting):
    # ------------------------------
    # Class attributes
    HopNum      = 0
    RTT         = 0
    RouterName  = ""
    RouterIP    = ""
    _Timeout    = False
    # ------------------------
    def __init__(self, dataString):
        #Inheritting our formatting and error handling
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding * 3
        if not isinstance(dataString, str):
            ValueError("Argument 'dataString' must be a string")
        #END IF
        self.Pings = []
        #Now we do the real parsing
        firstSplit = dataString.strip().split(" ",1)
        self.HopNum = int(firstSplit[0].strip())
        #This will check if all of the Pings in this Hop were timeouts, which
        # are represented by '*'
        if firstSplit[1].count("*") == 3:
            self._Timeout = True
            self.RTT = -1
            return
        #END IF

        #Now we will split on spaces, and check that we get at least 3 non-empty
        # elements (the router name, IP, and RTT)
        HopSplit = firstSplit[1].split(" ")
        HopSplit = [info for info in HopSplit if info]
        #Checking that there wasn't a weird error of some kind
        if len(HopSplit) != 3:
            self.ContainsErrors = True
            self.ErrorCode = 404
        #END IF

        #We now get the router name, IP, and RTT from our now array of 3 elements
        self.RouterName = HopSplit[0].strip()
        self.RouterIP = HopSplit[1].split(")")[0].split("(")[1].strip()
        self.RTT = float(HopSplit[2].split("ms")[0].strip())

        '''
        #Now we go through each Ping, and if it only contains the RTT value, then
        # we use the first Ping's name and IP. We will use a regular expression
        # search to search for an IP address. If one is not found, then we can
        # assume that the Ping has the same information as the first
        from re import search
        for ping in pingsSplit:
            #This will search for something that contains a "(", followed by at
            # least 1 number of any kind, then a ".", which is found using "\.".
            # The at least 1 number of any kind is matched, followed by a ".". This is how
            # we find if there was an IP address. ex. (12.211.54.183) will be found by this
            if search("\([0-9]+\.[0-9]+\.", ping):
                firstPingName = ping.split(")")[0].split("(")[0].strip()
                firstPingIP = ping.split(")")[0].split("(")[1].strip()
                pingRTT = float( ping.split(")")[1].strip() )
            else:
                pingRTT = float( ping.strip() )
            #END IF/ELSE
            #Using the above values parsed to create a Ping object, and appending
            # it to our array in self.Pings
            self.Pings.append( Ping(firstPingName, firstPingIP, pingRTT) )
        #END FOR

        #One last little declaration for this object, calculating the average RTT for
        # this traceroute test. Using the built in statistics module
        from statistics import mean
        #This list comprehension will calculate the average RTT for the 1+ Pings in this
        # Hop. It will first remove the values less than 0, and then use statistics' mean()
        # function to get the average
        self.AvgRTT = mean( [value for value in self.get_RTTsAsArray() if (value>0)] )
        '''
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        if self._Timeout:
            return ( self.StringPadding +
                        str(self.HopNum) + ("   " if self.HopNum<10 else "  ") + "* * *")
        else:
            return ( self.StringPadding +
                        str(self.HopNum) + ("   " if self.HopNum<10 else "  ") +
                        str(self.RouterName) + "  ("+str(self.RouterIP)+")  " +
                        str(self.RTT)+" ms")
        #END IF/ELSE
    #END DEF
#END CLASS





"""
------------------------------------------------------------------------
TCRT_TEST Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual trace route test. This class keeps track of the
            RTT values for each step along the route, as well as information on the hop.

VARIABLES:
  INHERITED
    ConnectionType      String, represents the type of connection (TCP, UDP, PING, or TRACERT)
    ConnectionLoc       String, represents where this test is connected to (East or West)
    TestNumber          Integer, the number of this test (order in which it was run)
    StartingLine        String, the first line of text in this whole test
    _text               List of Strings, the raw data, split by '\n'
  NOT INHERITED
    Hops                List, contains all of the Hop objects associated with this test
    MaxHops             Integer, the maximum number of hops this test will have
    PacketSize          Integer, the size (in bytes) that the ping packets were

FUNCTIONS:
  INITIALIZATION
    __init__ - Used to initialize an object of this class
        INPUTS-     self:           reference to the object calling this method (i.e. Java's THIS)
                    dataString:     String, the text that is going to be parsed
                    isMobile:       Boolean, whether this test was taken on a mobile or netbook device
                    short:          Boolean, whether to print this object in short or long form
        OUTPUTS-    none
    parseHops - Parses out all of the Ping test information (individual ping RTTs and total RTT stats)
                from the text stored in self._text
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    none

  GETTERS
    get_RTTsAsArray - Returns a list of the Hop's RTT values, for more simple use by other scripts
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values in the objects in self.Hops in sequence
    //get_csvDefaultValues - Returns a List of the default CSV values needed for the creation of a CSV
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    List, the values necessary for the creation of the CSV file

  STRING PRINOUT
    __str__ - Returns a string representation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
------------------------------------------------------------------------
"""

# IMPORTS
from PyObjects._Test import Test
#END IMPORTS

# CLASS
class TCRT_Test(Test):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ConnectionType  = ""
    # ConnectionLoc   = ""
    # TestNumber      = 0
    # ReceiverIP      = ""
    # StartingLine    = ""
    # _text           = ""

    # Class attributes
    Hops        = None
    MaxHops     = 0
    PacketSize  = 0
    # ------------------------


    # DESC: Initializing class
    def __init__(self, dataString="", eastWest=("0.0.0.0", "0.0.0.0")):
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWest=eastWest)
        self.Hops = {}

        #We need to get some basic information from the traceroute command call
        I_need_this = None
        for line in self._text:
            if "traceroute to" in line:
                I_need_this = line
                break
        #END FOR
        #Setting some basic information
        if I_need_this:
            info = I_need_this.split(",")
            self.MaxHops = int(info[1].split("hops")[0].strip())
            self.PacketSize = int(info[2].split("byte")[0].strip())
        #END IF

        #Now we parse out the Hops from the test text (in dataString)
        if not self.ContainsErrors:
            '''
            This may be used later, if it is found that there can be different outputs

            #We need to first figure out if the test is from a mobile device,
            # or netbook (for Field Test files). This also differentiates between Phone
            # and Desktop in Crowd Source files.
            if "Ping statistics for" not in dataString:
                self.is_outputType1 = True
            else:
                self.is_outputType1 = False
            #END IF/ELSE
            '''
            self.parseHops()
        #END IF
        #Clearing the values in self._text so we don't waste some space
        self._text = None
    #END DEF


# Intialization Functions ----------------------------------------------------------------

    # DESC: Parses out all of the Ping test information (individual ping RTTs and total RTT stats) from the text
    def parseHops(self):
        #We are going to loop through each line in self._text. If the line is a Hop line
        # (where it contains either 'ms' or '*'), then we pass it to our Hop class, and
        # append the object to self.Hops.
        for line in self._text:
            if any( [(text in line) for text in ["ms","*"]] ):
                newHop = Hop(dataString=line)
                self.Hops[newHop.HopNum] = newHop
            #END IF
        #END FOR
    #END DEF


# Getter - Times as array of nums --------------------------------------------------------------

    # DESC: Returns the times stored in this object Times attribute as an array of numbers
    def get_RTTsAsArray(self):
        keys = list(self.Hops.keys())
        keys.sort()
        return [ self.Hops[key].RTT for key in keys ]
    #END DEF

    # DESC: Returns an array of the necessary values for the CSV file being created
    def get_csvDefaultValues(self):
        csvVals = []
        if not self.ContainsErrors:
            csvVals = [""]*4
            '''
            csvVals.append(self.RTTMin)
            csvVals.append(self.RTTMax)
            csvVals.append(self.RTTAverage)
            LossPercent = int(float(self.PacketsLost)*100/self.PacketsSent)
            csvVals.append(LossPercent)
            '''
        else:
            csvVals = [self.ErrorTypes[self.ErrorCode]]*4
        return csvVals
    #END DEF

# String printout ------------------------------------------------------------------------------

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
                    "Max Hops: " + str(self.MaxHops) +
                    "  Packet Size: " + str(self.PacketSize) + " bytes\n" +
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
            keys = list(self.Hops.keys())
            keys.sort()
            for key in keys:
                string += (str(self.Hops[key]) +"\n")
        #END IF
        return string
    #END DEF
#END CLASS
