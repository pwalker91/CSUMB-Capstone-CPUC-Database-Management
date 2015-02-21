"""
------------------------------------------------------------------------
_THREAD.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will represent a single thread, or pipe, in a network
            speed test. It will hold an array of Measurement objects, and has
            some basic object information

FUNCTIONS:
    __init__
    arrayOfMsmts
    __str__
------------------------------------------------------------------------
"""


# IMPORTS
from __Base import Formatting
from _Measurement import Measurement as Msmt
from _Measurement import Final_Measurement as FMsmt
#END IMPORTS

# CLASS
class Thread(Formatting):
    # ----------------------------------
    # Class attributes
    ThreadNumber    = 0
    DataDirection   = ""

    LocalIP         = ""
    LocalPort       = 0
    ServerIP        = ""
    ServerPort      = 0

    Measurements    = []
    FinalMsmt       = None
    # ----------------------------------

    def __init__(self, dataArr=None, threadNum=0, direction="UP", units=("KBytes", "Kbits/sec")):
        """
        Used to initialize an object of this class
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
            dataArr:    List of Strings, each String is a measurement that will be parsed and stored in this object
            ThreadNum:  Integer, the number that this thread is (generally between 3 and 6)
            direction:  String, the direction of the data in this thread (UP or DOWN)
            units:      Tuple of two Strings, the units being used by the measurements
        """
        #Setting up the whitespace padding that this class will need
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding*3
        #Class variables
        self.Measurements = []
        self.ThreadNumber = threadNum
        self.DataDirection = direction
        #This function assumes that the array of strings (dataArr) is not in order
        #This takes the given data String and parses the object information
        for line in dataArr:
            if "connected with" in line:
                line            = line.split("local", 1)[1].strip()
                self.LocalIP    = line.split("port")[0].strip()
                line            = line.split("port", 1)[1].strip()
                self.LocalPort  = line.split("connected")[0].strip()
                line            = line.split("connected with", 1)[1].strip()
                self.ServerIP   = line.split("port", 1)[0].strip()
                line            = line.split("port", 1)[1].strip()
                self.ServerPort = line.split("\n")[0].strip()
                break
            #END IF
        #END FOR
        #Removing the line from the array of pings that contains the connection info
        # and then creating all of the pings from the remaining strings
        allMeasurements = [line for line in dataArr if "connected with" not in line]
        for line in allMeasurements:
            #We do a quick check for the string stored in units[1]. If that string is
            # present in a line, then it must be a measurement that we want to parse
            if (units[1] in line) and ("%" not in line):
                #Make a measurement object out of the line.
                newMsmt = Msmt(data=line, units=units)
                #If the measurement's start time is one second behind it's end time, then
                # we can assume that this is one of interval measurements. Otherwise, it is
                # the final summary measurement, and we put the object in self.FinalMsmt
                if (newMsmt.TimeStart == newMsmt.TimeEnd-1):
                    #This is for the UDP 1 second tests, where this only 1 regular
                    # measurement, and then a final measurement. We delete the old object,
                    # and create a new one of type Final_Measurement
                    if (newMsmt.TimeStart == 0) and (len(self.Measurements) == 1):
                        del newMsmt
                        FinalMsmt = FMsmt(data=line, units=units)
                        self.FinalMsmt = FinalMsmt
                        break
                    else:
                        self.Measurements.insert(int(newMsmt.TimeStart), newMsmt)
                    #END IF/ELSE
                else:
                    del newMsmt
                    FinalMsmt = FMsmt(data=line, units=units)
                    self.FinalMsmt = FinalMsmt
                #END IF/ELSE
            #END IF
        #END FOR
    #END DEF

    def arrayOfMsmts(self, attribute="Speed"):
        """
        Will return an array of the Measurements in self.Measurements as an array
        of Numbers. Can be given the attribute of the measurement that needs to be arraytized
        ARGS:
            self:       reference to the object calling this method (i.e. Java's THIS)
            attribute:  String, can be "speed" or "size" (attribute of Measurment)
        RETURNS:
            list, containing all of the values in the Measurement object of myMeasurements
        """
        if attribute not in ["Speed", "Size"]:
            print("The attribute specified must be either 'Speed' or 'Size'. Using 'Speed'")
            attribute = "Speed"
        #END IF
        #This uses list comprehension to return a list of all of the measurement's attribute,
        # specified by the variable attribute
        return [msmt.__dict__[attribute] for msmt in self.Measurements]
    #END DEF


# String printout ------------------------------------------------------------------------------

    def __str__(self):
        """Returns a string representation of the object"""
        string = (self.StringPadding +
                    "Thread Number: " + str(self.ThreadNumber) +"\n" +
                  self.StringPadding +
                    "Data Direction: " + str(self.DataDirection) +"\n" +
                  self.StringPadding +
                    "Local: "+ str(self.LocalIP) +":"+ str(self.LocalPort) +"\n" +
                  self.StringPadding +
                    "Server: "+ str(self.ServerIP) +":"+ str(self.ServerPort) +"\n"
                 )
        for msmt in self.Measurements:
            string += str(msmt) + "\n"
        string += str(self.FinalMsmt) + "\n"
        return string
    #END DEF
#END CLASS
