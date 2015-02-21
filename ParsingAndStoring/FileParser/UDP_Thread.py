"""
------------------------------------------------------------------------
UDP_THREAD.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will represent a single thread, or pipe, in a network
            speed test. It will hold an array of Measurement objects, and has
            some basic object information

FUNCTIONS:
    __init__
    __str__
------------------------------------------------------------------------
"""


# IMPORTS
from _Thread import Thread
from _Measurement import UDP_ServerReport as ServerReport
#END IMPORTS

# CLASS
class UDP_Thread(Thread):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ThreadNumber    = 0
    # DataDirection   = ""
    # LocalIP         = ""
    # LocalPort       = 0000
    # ServerIP        = ""
    # ServerPort      = 0000
    # Measurements    = []
    # FinalMsmt       = None

    # Class attributes
    DatagramzSent = 0
    ServerReport = None
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
        #Call the parent class' __init__
        Thread.__init__(self, dataArr=dataArr, threadNum=threadNum, direction=direction, units=units)
        #Parsing out the datagrams sent, and the server report (which is passed to the UDP_ServerReport object)
        for line in dataArr:
            #These two lines below check that the correct line is gotten.
            # First initialize an array of strings (which will be used as reference).
            # Next, for each elem in the array, check if it is in the line we are checking.
            #   (this is everything in the parenthesis)
            # Then, use all() on the returned array. The code in the parenthesis returns an array of
            #  booleans, and all() makes sure that they are all True.
            # If the conditions are met, this line is the line we are looking for.
            # If one of the strings was not found, then sadly, it means
            #  that these are not the droids we are looking for...
            # This was implemented because datagrams is in a few other lines, but not the ones we want
            strCheck = ["datagrams", "Sent"]
            if all([text in line for text in strCheck]):
                self.DatagramzSent = int(line.split("Sent ")[1].split(" ")[0])
            # If "Server Report" is in the line, we need the next line
            if "Server Report" in line:
                #The actual server report is the line below the current line, so we need to get
                # this current line's index, and add 1 to it
                tempIndex = dataArr.index(line) + 1
                serverReportLines = []
                #This uses list comprehension to get all of the lines pertaining to the Server Report.
                # Sometimes, there is more than one line in the Server Report
                [serverReportLines.append(line) for line in dataArr[tempIndex:] if ("[ " in line)]
                #Passing the necessary lines to the Server Report constructor
                self.ServerReport = ServerReport(data=serverReportLines, units=units)
            #END IF/ELIF
        #END FOR
    #END DEF


# String printout ------------------------------------------------------------------------------

    def __str__(self):
        """Returns a String representation of the object"""
        string = (self.StringPadding +
                    "Thread Number: " + str(self.ThreadNumber) + "\n" +
                  self.StringPadding +
                    "Data Direction: " + str(self.DataDirection) + "\n" +
                  self.StringPadding +
                    "Local: " + str(self.LocalIP) +":"+ str(self.LocalPort) + "\n" +
                  self.StringPadding +
                    "Server: " + str(self.ServerIP) +":"+ str(self.ServerPort) + "\n" +
                  self.StringPadding +
                    "Datagrams Sent: " + str(self.DatagramzSent) + "\n"
                 )
        for msmt in self.Measurements:
            string += str(msmt) +"\n"
        string += ( str(self.FinalMsmt) +"\n"+ str(self.ServerReport) +"\n" )
        return string
    #END DEF
#END CLASS
