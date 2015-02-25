"""
------------------------------------------------------------------------
TCP_TEST.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This class will hold just an individual TCP speed test.
            This takes a chunk of text (as a string), and parses out all of the header information,
            like the server connected to, measuring format, etc. It then splits the test measurements
            into their individual threads, and passing the resulting strings to the Thread object.

FUNCTIONS:
  INITIALIZATION:
    __init__
    parseThreads
    checkForOutputErrors
  THREAD VALUE GETTERS
    get_ThreadSumValues
    get_ThreadsValues
  FOR STAT ANALYSIS (append to CSV)
    get_csvDefaultValues
    get_csvStatValues
    get_csvQualValues
  STRING PRINTOUT
    __str__
------------------------------------------------------------------------
"""


# IMPORTS
from statistics import pstdev, median
from _Test import Test
from TCP_Thread import TCP_Thread
#END IMPORTS

# CLASS
class TCP_Test(Test):
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

    # Class attributes
    ThreadsByNum    = None
    WindowSize      = 0
    ThreadNumbers   = None
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
        #If we were unable to parse out the iPerfCommand line from the text, then
        # we assume that there was an error of some kind that was not caught, and exit
        if not self.iPerfCommand:
            raise RuntimeError("For some reason, the Iperf command line was not parsed.")
        #Getting the window size
        self.WindowSize = self.iPerfCommand[self.iPerfCommand.find("-w"):].split(" ")[1].strip()
        if not self.ContainsErrors:
            #Declaring and creating the Ping Threads for this test
            self.Threads = { "UP" : [], "DOWN" : [] }
            self.ThreadsByNum = {}
            #This will run the function that creates the Ping Threads, but will only
            # clear self.text if there were no errors
            self.parseThreads()
            #Doing a few more checks for errors
            if not self.ContainsErrors:
                self.checkForOutputErrors()
        #END IF
    #END DEF


# Intialization Functions ----------------------------------------------------------------

    def parseThreads(self):
        """
        Given the data stored in self._text, parses the Iperf output into individual TCP_Threads
        """
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
        oneLess = 0; oneMore = 0
        for threadNum, value in checkThreadsForErr.items():
            if value == 3:
                oneMore = threadNum
                self.ContainsErrors = True
            if value == 1:
                oneLess = threadNum
                self.ContainsErrors = True
        #END FOR
        #If an error was found, then we need to set the appropiate messages, and then exit this function
        if self.ContainsErrors:
            self.ErrorCode = 101
            self.ErrorMessages[101] = ("There was an error in the TCP test output. "+
                                    "Threads #" +str(oneMore)+ " had one extra thread start,"+
                                    " and #" +str(oneLess)+ " had one less." )
            self.Threads = {}
            #If there was an error, then we return with what amounts to an empty TCP Test
            return
        #END IF

        #Now that every thread is sorted into an array of string, we can split them into
        # upload and download threads, and pass it to the TCP_Thread object
        #Grabbing a list of all of the thread numbers from this test
        self.ThreadNumbers = list(tempThreads.keys())
        #Initializaing tempThreadsByDirection to have the necessary keys (thread numbers),
        # and each key holds another dictionary of 2 arrays, linked to the keys UP and DOWN
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
        err_threadNum = 0; err_threadDir = ""
        for threadNum in tempThreadsByDirection:
            for direction in tempThreadsByDirection[threadNum]:
                if len(tempThreadsByDirection[threadNum][direction]) < 3:
                    self.ContainsErrors = True
                    err_threadNum = threadNum; err_threadDir = direction
                    break
            #END FOR
        #END FOR
        #If an error was found, then we need to set the appropiate messages, and then exit this function
        if self.ContainsErrors:
            self.ErrorCode = 101
            self.ErrorMessages[101] = ("There was an error in the TCP test output. "+
                                    "Threads #" +str(err_threadNum)+ " in the "+err_threadDir+
                                    " direction did not have enough measurements" )
            self.Threads = {}
            #If there was an error, then we return with what amounts to an empty TCP Test
            return
        #END IF

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

    def checkForOutputErrors(self):
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
                if thread.FinalMsmt.TimeStart == thread.FinalMsmt.TimeEnd:
                    self.ContainsErrors = True
                    self.ErrorCode = 101
                    self.ErrorMessages[101] = (direction + " Thread #" + str(thread.ThreadNumber) +" had a bad " +
                                            "final measurement. (Time was from 0.0 to 0.0 seconds)")
                    break
                if (thread.FinalMsmt.Speed > 1000000) and (thread.Measurements[0].Speed == 0):
                    self.ContainsErrors = True
                    self.ErrorCode = 101
                    from math import log10
                    self.ErrorMessages[101] = (direction + " Thread #" + str(thread.ThreadNumber) +" had a bad " +
                                            "final measurement. (Measured speed was in the order of 10^" +
                                            str(int(log10(thread.FinalMsmt.Speed))) + ")")
                    break
                #END IF/ELIF
            #END FOR
        #END FOR
        if self.ContainsErrors:
            self.Threads = {}
            self.ThreadsByNum = {}
        #END IF
    #END DEF


# Thread value Getters -------------------------------------------------------------------

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
                try: temp += array[interval]
                except: pass
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


# For statistical analysis ----------------------------------------------------------------------

    def get_csvDefaultValues(self):
        """
        Returns a List of the default CSV values needed for the creation of a CSV
        """
        csvVals = []
        #If there was no error, there are values to calculate
        # Otherwise, we return an array of "self._error_Type"
        if not self.ContainsErrors:
            upSum = 0; dnSum = 0
            for thread in self.Threads["UP"]:
                upSum += thread.FinalMsmt.Speed
            for thread in self.Threads["DOWN"]:
                dnSum += thread.FinalMsmt.Speed
            csvVals = [upSum, dnSum]
        else:
            csvVals = [self.ErrorTypes[self.ErrorCode]]*2
        return csvVals
    #END DEF

    def get_csvStatValues(self):
        """
        This creates an array of 4 values that will be appended to the Results CSV
        provided by CPUC. If there was an error in the test, the 4 values returned are the error type.
        Otherwise, the 4 values are the StDev and Median for both thread directions for this test
        """
        csvVals = []
        #If there was no error, there are values to StDev and Median
        # Otherwise, we return an array of "None"
        if not self.ContainsErrors:
            #Calculating the stDev's and medians of the Up and Down threads
            upThread = self.get_ThreadSumValues(direction="UP", attribute="Speed")
            downThread = self.get_ThreadSumValues(direction="DOWN", attribute="Speed")
            csvVals.append( pstdev(upThread) )
            csvVals.append( median(upThread) )
            csvVals.append( pstdev(downThread) )
            csvVals.append( median(downThread) )
        else:
            csvVals = [self.ErrorTypes[self.ErrorCode]]*4
        return csvVals
    #END DEF

    def get_csvQualValues(self):
        """
        This function calculates the quality of the TCP connection.
        Quality is determined by either Time or Data. Time is the average total time it took for
        the TCP threads to complete transfer. Data is a score between 1 and 0, where
        a time interval is given a 1 if it is transmitting data, and a 0 if it is not. The 1's
        and 0's are totaled up and averaged.
        """
        qualVals = []
        #If there are not errors, then we calculate the quality of the test. Otherwise, we
        # we return a List of the error type
        if not self.ContainsErrors:
            ttlUpTime   = float(0); numUpThreads = 0
            upPosSpeeds = float(0); numUpSpeeds  = 0
            ttlDnTime   = float(0); numDnThreads = 0
            dnPosSpeeds = float(0); numDnSpeeds  = 0
            #This block calculates the TCP Quality based on the total time
            # it took the thread to complete their downloads
            #For each thread, get the total time (final measurement timeEnd)
            for thread in self.Threads["UP"]:
                ttlUpTime += thread.FinalMsmt.TimeEnd
                numUpThreads += 1
            #END FOR
            for thread in self.Threads["DOWN"]:
                ttlDnTime += thread.FinalMsmt.TimeEnd
                numDnThreads += 1
            #END FOR
            #This block calculates the TCP Quality based on the data score,
            # a value between 1 and 0 based on how many intervals in the threads were
            # either downloading or uploading data
            speeds = self.get_ThreadsValues(direction="UP")
            #This adds the number of intervals from each thread to the numUpSpeeds variable,
            # and will be used later to calculate the score (between 1 and 0)
            numUpSpeeds += sum( [len(thread) for thread in speeds] )
            for thread in speeds:
                for elem in thread:
                    if elem > 0: upPosSpeeds+=1
            #END FOR
            speeds = self.get_ThreadsValues(direction="DOWN")
            numDnSpeeds += sum( [len(thread) for thread in speeds] )
            for thread in speeds:
                for elem in thread:
                    if elem > 0: dnPosSpeeds+=1
            #END FOR
            #This append the values to the array. The values are the TCP UP quality based
            # on time, then number of non-zero speeds, then the TCP DOWN quality based on
            # time, then number of non-zero speeds
            qualVals = [(ttlUpTime/numUpThreads), (upPosSpeeds/numUpSpeeds),
                        (ttlDnTime/numDnThreads), (dnPosSpeeds/numDnSpeeds) ]
        else:
            qualVals = [self.ErrorTypes[self.ErrorCode]]*4
        #DND IF/ELSE
        return qualVals
    #END DEF


# String printout -------------------------------------------------------------------------------

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (self.StringPadding +
                    "Test Number: " + str(self.TestNumber) + "\n" +
                  self.StringPadding +
                    "Connection Type: " + str(self.ConnectionType) + "\n" +
                  self.StringPadding +
                    "Connection Location: " + str(self.ConnectionLoc) + "\n" +
                  self.StringPadding +
                    "Receiver IP: " + str(self.ReceiverIP) + ":" + str(self.Port) + "\n" +
                  self.StringPadding +
                    "Test Interval: " + str(self.TestInterval) +
                    "  Window Size: " + str(self.WindowSize) +
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
