"""
------------------------------------------------------------------------
TCRT_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual trace route test. This class keeps track of the
            RTT values for each step along the route, as well as information on the hop. This
            class uses a sub-class included in this file, the Hop class.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
from __Base import Formatting
#END IMPORTS




"""
------------------------------------------------------------------------
HOP Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual hop within the traceroute. This object
            essentially represents one line in the test
------------------------------------------------------------------------
"""


class Hop(Formatting):

    """A single traceroute 'hop', which is the router IP, name, and RTT"""

    '''
    # ------------------------------
    # ---- CLASS ATTRIBUTES ----
    HopNum      = 0
    RTT         = 0.0
    RouterName  = ""
    RouterIP    = ""
    _Timeout    = False
    # ------------------------------
    '''


    def __init__(self, dataString):
        """
        Used to initialize an object of this class
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            dataString: String, the raw text that will be parsed
        """
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
            self._ErrorHandling__setErrorCode(404)
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

    def __str__(self):
        """Creating a string representation of our object"""
        if self._Timeout:
            return (self.StringPadding +
                    str(self.HopNum) + ("   " if self.HopNum<10 else "  ") + "* * *"
                    )
        else:
            return (self.StringPadding +
                    str(self.HopNum) + ("   " if self.HopNum<10 else "  ") +
                    str(self.RouterName) + "  ("+str(self.RouterIP)+")  " +
                    str(self.RTT)+" ms"
                    )
        #END IF/ELSE
    #END DEF
#END CLASS





"""
------------------------------------------------------------------------
TCRT_TEST Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold an individual trace route test. This class keeps track of the
            RTT values for each step along the route, as well as information on the hop.

FUNCTIONS:
  INITIALIZATION
    __init__
    parseHops
  GETTERS
    get_RTTsAsArray
    get_csvDefaultValues        !!!
  STRING PRINOUT
    __str__
------------------------------------------------------------------------
"""

# IMPORTS
import sys
from _Test import Test
#END IMPORTS


class TCRT_Test(Test):

    """
    A Traceroute Test, which are the RTTs from the device running the test
     to all routers along a network path to a specified destination
    """

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
    Hops        = None
    MaxHops     = 0
    PacketSize  = 0
    # ------------------------
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
        if "traceroute" not in dataString.lower():
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (TCRT_Test) did not contain "+
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
        #If we are at this point, then the dataString contained "traceroute", and we can
        # set the ConnectionType to "TCRT"
        self.ConnectionType = "TCRT"
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)
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
    #END DEF


# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def parseHops(self):
        """
        Parses out all of the Ping test information (individual ping RTTs and total RTT stats)
        from the text stored in self._text
        """
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


# GETTERS ----------------------------------------------------------------------

    def get_RTTsAsArray(self):
        """
        Returns a list of the Hop's RTT values, for more simple use by other scripts
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
        RETURNS:
            List, the values in the objects in self.Hops in sequence
        """
        keys = sorted(list(self.Hops.keys()))
        return [ self.Hops[key].RTT for key in keys ]
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
                  "Max Hops: {}".format(self.MaxHops) +
                  "  Packet Size: {} bytes\n".format(self.PacketSize) +
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
            keys = sorted(list(self.Hops.keys()))
            for key in keys:
                string += (str(self.Hops[key]) +"\n")
        #END IF
        return string
    #END DEF
#END CLASS
