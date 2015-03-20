"""
------------------------------------------------------------------------
TCP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual TCP speed test.
            This takes a chunk of text (as a string), and parses out all of the header information,
            like the server connected to, measuring format, etc. It then splits the test measurements
            into their individual threads, and passing the resulting strings to the Thread object.
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
import sys
from statistics import pstdev, median
from _Test import Test
from TCP_Thread import TCP_Thread
#END IMPORTS


class TCP_Test(Test):

    """A TCP test, which is 4 Upload and 4 Download threads connected to a server"""

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
    ThreadsByNum    = None
    WindowSize      = 0
    ThreadNumbers   = None
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
        if "tcp" not in dataString.lower():
            if "DEBUG" in kwargs and kwargs["DEBUG"]:
                print("The raw data passed to this constructor (TCP_Test) did not contain "+
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
        self.ConnectionType = "TCP"
        #Call the parent class' __init__
        Test.__init__(self, dataString=dataString, eastWestIP=eastWestIP)

        #If we were unable to parse out the iPerfCommand line from the text, then
        # we assume that there was an error of some kind that was not caught, and exit
        if not self.iPerfCommand:
            self._ErrorHandling__setErrorCode(101, "Iperf Command Line not Found")
            #raise RuntimeError("For some reason, the Iperf command line was not parsed.")
        else:
            #Getting the window size
            self.WindowSize = self.iPerfCommand[self.iPerfCommand.find("-w"):].split(" ")[1].strip()
            if not self.ContainsErrors:
                #Declaring and creating the Ping Threads for this test
                self.Threads = {"UP":[],
                                "DOWN":[]
                                }
                self.ThreadsByNum = {}
                #This will run the function that creates the Ping Threads, but will only
                # clear self.text if there were no errors
                self.parseThreads()
                #Doing a few more checks for errors
                if not self.ContainsErrors:
                    self.__checkForOutputErrors()
            #END IF
        #END IF/ELSE
    #END DEF



# INITIALIZATION FUNCTIONS -----------------------------------------------------

    def parseThreads(self):
        """Given the data stored in self._text, parses the Iperf output into individual TCP_Threads"""
        #We first call the sorting method, which will return a boolean and the strings
        # in self._text sorted by thread number. If the boolean is true, the threads are sorted
        (sorted_, tempThreads) = self.__sortThreadsByNum()
        if not sorted_:
            return

        #Now that every thread is sorted into an array of string, we can split them into
        # upload and download threads, and pass it to the TCP_Thread object
        #Grabbing a list of all of the thread numbers from this test
        self.ThreadNumbers = list(tempThreads.keys())
        #Initializaing tempThreadsByDirection to have the necessary keys (thread numbers),
        # and each key holds another dictionary of 2 arrays, linked to the keys UP and DOWN
        (againSorted_, tempThreadsByDirection) = self.__sortThreadsByNumDir(tempThreads)
        if not againSorted_:
            return

        #Now that everything is split by thread number and by direction, we can call
        # the TCP Thread object creation
        for threadNum in tempThreadsByDirection:
            #Creating the TCP_Thread objects for the Upload and Download threads
            upThread = TCP_Thread(dataArr=tempThreadsByDirection[threadNum]["UP"],
                                  threadNum=threadNum, direction="UP",
                                  units=self.MeasuringFmt)
            downThread = TCP_Thread(dataArr=tempThreadsByDirection[threadNum]["DOWN"],
                                    threadNum=threadNum, direction="DOWN",
                                    units=self.MeasuringFmt)
            #Appending the TCP_Thread objects to their respective direction in self.Threads
            # and thread number / direction in ThreadsByNum
            self.Threads["UP"].append(upThread)
            self.Threads["DOWN"].append(downThread)
            self.ThreadsByNum[threadNum]["UP"] = upThread
            self.ThreadsByNum[threadNum]["DOWN"] = downThread
        #END FOR
    #END DEF

    def __sortThreadsByNum(self):
        #This block does the initial organization, going through each line and
        # putting them into the array whose key corresponds with their thread number.
        tempThreads = {}
        for line in self._text:
            if ("[" in line) and ("SUM" not in line):
                #This gets the thread number from within the square brackets, checks
                # if it is a key in tempThreads, and then adds the line to correct
                # list in tempThreads (each key is a thread number)
                newKey = int(line.split("]")[0][1:].strip())
                if newKey not in tempThreads.keys():
                    tempThreads[newKey] = []
                #END IF
                tempThreads[newKey].append(line)
            #END IF
        #END FOR

        #ERROR CHECKING
        #Now we check for a funny error, where one thread starts either an upload or download twice,
        # while another only starts an upload. If this is the case, the test will be ignored, and
        # self._contains_Errors is set to True.
        checkThreadsForErr = {}
        for threadNum, thread in tempThreads.items():
            #This line goes through all of the lines in thread, and counts how many have
            # "connected with" in them. If the line contains the string, it adds a 1, otherwise a 0.
            # At the end, it sums up the number of "connected with"s, and uses that in the next
            # block to determine if there was an output error
            checkThreadsForErr[threadNum] = sum( [1 if ("connected with" in line) else 0 for line in thread] )
        oneLess = 0
        oneMore = 0
        _wasAnError = False
        for threadNum, value in checkThreadsForErr.items():
            if value == 3:
                oneMore = threadNum
                _wasAnError = True
            if value == 1:
                oneLess = threadNum
                _wasAnError = True
        #END FOR
        #If an error was found, then we need to set the appropiate messages, and then exit this function
        if _wasAnError:
            specialMessage = ("There was an error in the TCP test output. "+
                              "Threads #" +str(oneMore)+ " had one extra thread start,"+
                              " and #" +str(oneLess)+ " had one less." )
            self._ErrorHandling__setErrorCode(101, specialMessage)
            self.Threads = {}
            #If there was an error, then we return with what amounts to an empty TCP Test
            return (False, None)
        #END IF
        return (True, tempThreads)
    #END DEF

    def __sortThreadsByNumDir(self, tempThreads):
        tempThreadsByDirection = {}
        for threadNum in self.ThreadNumbers:
            tempThreadsByDirection[threadNum] = {"UP": [], "DOWN": []}
            self.ThreadsByNum[threadNum] = {"UP": None, "DOWN": None}
        #Now we can actually start putting the necessary strings into the arrays
        # that they need to be sorted into. This will make the structure below
        # dict [thread number 1] [ UP ]   = [String1, String2, String3, etc..]
        #      [thread number 1] [ Down ] = [String4, String5, String6, etc..]
        #      [thread number 2] [ UP ]   = [String7, String8, String9, etc..]
        #      .....
        for threadNum, thread in tempThreads.items():
            downStartInd = 0
            for elem in thread[1:]:
                if "connected with" in elem:
                    downStartInd = thread[1:].index(elem) + 1
                    break
            #END FOR
            #We slice up the array of strings in thread, putting the upload ones
            # in [threadNum]["UP"], and the download ones into [threadNum]["DOWN"]
            tempThreadsByDirection[threadNum]["UP"] = thread[0:downStartInd]
            tempThreadsByDirection[threadNum]["DOWN"] = thread[downStartInd:]
        #END FOR

        #ERROR CHECKING
        #One last check for another funny error. This is where the thread only had
        # one good measurement (from 0.0 to 1.0). We check the length of the array,
        # and if it is less than 3, then we have that funny error.
        err_threadNum = 0
        err_threadDir = ""
        _wasAnError = False
        for threadNum in tempThreadsByDirection:
            for direction in tempThreadsByDirection[threadNum]:
                if len(tempThreadsByDirection[threadNum][direction]) < 3:
                    _wasAnError = True
                    err_threadNum = threadNum
                    err_threadDir = direction
                    break
            #END FOR
        #END FOR
        #If an error was found, then we need to set the appropiate messages, and then exit this function
        if _wasAnError:
            specialMessage = ("There was an error in the TCP test output. "+
                              "Threads #" +str(err_threadNum)+ " in the "+err_threadDir+
                              " direction did not have enough measurements" )
            self._ErrorHandling__setErrorCode(101, specialMessage)
            self.Threads = {}
            #If there was an error, then we return with what amounts to an empty TCP Test
            return (False, None)
        #END IF
        return (True, tempThreadsByDirection)
    #END DEF

    def __checkForOutputErrors(self):
        """
        After all of the threads have been initialized, this function checks for
        some special cases of output errors, i.e. final measurement is 0.0 - 0.0 sec,
        final msmt download speed is in the order to 10^16, or 10 Quadrillion Kbits/sec
        """
        #Checking for 0.0 - 0.0 sec final measurement
        for direction, threads in self.Threads.items():
            #We are going to loop through each thread in each direction to check
            # for our weird output error
            for thread in threads:
                #If the start time and end time of the final measurement
                # are the exact same, then there is a weird error. We set the boolean
                # to true, and clear this object of thread objects
                if not thread.FinalMsmt:
                    specialMessage = (direction + " Thread #{}".format(thread.ThreadNumber) +
                                      " had no final measurement in it's output.")
                    self._ErrorHandling__setErrorCode(101, specialMessage)
                    break
                if thread.FinalMsmt.TimeStart == thread.FinalMsmt.TimeEnd:
                    specialMessage = (direction + " Thread #{}".format(thread.ThreadNumber) +
                                      " had a bad final measurement. (Time was from 0.0 to 0.0 seconds)")
                    self._ErrorHandling__setErrorCode(101, specialMessage)
                    break
                if (thread.FinalMsmt.Speed > 1000000) and (thread.Measurements[0].Speed == 0):
                    from math import log10
                    specialMessage = (direction + " Thread #{}".format(thread.ThreadNumber) +
                                      " had a bad final measurement. (Measured speed was in the order "+
                                      "of 10^{})".format(int(log10(thread.FinalMsmt.Speed)))
                                      )
                    self._ErrorHandling__setErrorCode(101, specialMessage)
                    break
                #END IF/ELIF
            #END FOR
        #END FOR
        if self.ContainsErrors:
            self.Threads = {}
            self.ThreadsByNum = {}
        #END IF
    #END DEF



# THREAD VALUE GETTERS ---------------------------------------------------------

    def get_ThreadSumValues(self, direction="DOWN", attribute="Speed"):
        """
        Creating an array of the sum of each 1 second interval of all 4 thread's speed or size
        ARGS:
            self:           reference to the object calling this method (i.e. Java's THIS)
            direction:      String, threads of specified direction (Up or Down) that will be summed
            attribute:      String, the attribute of the measurement we wish to sum up (speed or size)
        RETURNS:
            threads_summed: an array containing values representing the sum of each 4 threads' speed
        """
        #Just in case what was passed is not a possible option, we will chose the defaults
        if attribute not in ["Speed", "Size"]:
            attribute = "Speed"
        if direction not in self.Threads.keys():
            direction = "DOWN"
        #END IF
        #Getting all of the necessary values from the TCP Thread objects we have
        allValues = self.get_ThreadsValues(direction, attribute)
        #Calculating max thread length
        maxThreadLength = max( [len(array) for array in allValues] )
        #Get the sums of the "direction" threads. The first FOR loop will iterate X number of times
        # based on what is in maxThreadLength. Within the FOR loop, we set up
        # a temporary variable. We then try to add a specific interval (e.g. 1.0-2.0 sec) for each
        # thread to the temporary variable. If the interval does not exist, then nothing is added
        # (i.e. we add 0). We then append this value to threads_summed, which will be returned.
        threads_summed = []
        for interval in range(maxThreadLength):
            temp = 0
            for array in allValues:
                try:
                    temp += array[interval]
                except:
                    pass
            #END FOR
            threads_summed.append(temp)
        #END FOR
        return threads_summed
    #END DEF

    def get_ThreadsValues(self, direction="DOWN", attribute="Speed"):
        """
        Creating an array of array of speed for each 1 second interval for each thread in the test
        ARGS:
            self:           reference to the object calling this method (i.e. Java's THIS)
            direction:      String, threads of specified direction (Up or Down) that will be summed
            attribute:      String, the attribute of the measurement we wish to sum up (speed or size)
        RETURNS:
            threads_summed: an array containing values representing the sum of each 4 threads' speed
        """
        #Just in case what was passed is not a possible option, we will chose the defaults
        if attribute not in ["Speed", "Size"]:
            attribute = "Speed"
        if direction not in self.Threads.keys():
            direction = "DOWN"
        #END IF
        return [ thread.arrayOfMsmts(attribute) for thread in self.Threads[direction] ]
    #END DEF



# STRING PRINTOUT --------------------------------------------------------------

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (self.StringPadding[:-1] + "-" +
                  "Test Number: {}\n".format(self.TestNumber) +
                  self.StringPadding +
                  "Connection Type: {}\n".format(self.ConnectionType) +
                  self.StringPadding +
                  "Connection Location: {}\n".format(self.ConnectionLoc) +
                  self.StringPadding +
                  "Receiver IP: {}:{}\n".format(self.ReceiverIP,self.Port) +
                  self.StringPadding +
                  "Test Interval: {}".format(self.TestInterval) +
                  "  Window Size: {}".format(self.WindowSize) +
                  "  Measurement Format: {}, {}\n".format(self.MeasuringFmt[0],
                                                          self.MeasuringFmt[1]) +
                  self.StringPadding +
                  "Contain Errors: {}\n".format(repr(self.ContainsErrors)) +
                  ((self.StringPadding +"Error Type: "+self.ErrorType+"\n")
                   if self.ContainsErrors else ""
                   ) +
                  ((self.StringPadding +"Error Message: "+self.ErrorMessage+"\n")
                   if self.ContainsErrors else ""
                   )
                  )
        #Printing out the Threads, if the test did not contain errors
        if not self.ContainsErrors:
            for threadNum in self.ThreadNumbers:
                string += str(self.ThreadsByNum[threadNum]["UP"])
            for threadNum in self.ThreadNumbers:
                string += str(self.ThreadsByNum[threadNum]["DOWN"])
            #END FOR
        #END IF
        return string
    #END DEF
#END CLASS
