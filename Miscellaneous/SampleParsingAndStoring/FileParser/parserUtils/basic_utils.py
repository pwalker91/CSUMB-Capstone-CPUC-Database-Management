#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
BASIC_UTILS.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Provide a few functions that will be used in multiple modules

FUNCTIONS:
  COMMON PARSER FUNCTIONS
    getLinesWith
    isLessThanVersion
  MONTH ABBR/NUM CONVERSION
    monthAbbrToNum
    monthNumToAbbr
  STATISTICAL FUNCTIONS
    calcArray_OutliersRemoved
  TEST ANALYSIS
    calcTCPThroughput
    calc_rVal_MOS
--------------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit


# COMMON PARSER FUNCTIONS ------------------------------------------------------

def getLinesWith(fileStream, delimiter):
    """
    Given a file stream, reads the stream finding all lines that contain the delimiter
    ARGS:
        fileStream:     FileStream object, called with open(FILEPATH, 'r')
        delimiter:      String, the text that you are looking for
    RETURNS:
        occurences:     List of Strings, containing the fully read line that contained the delimiter
    """
    #Saving the current cursor location of the file stream
    startingPlace = fileStream.tell()
    occurences = []
    line = "__"
    #While the delimiter is not in the line, read a line. If nothing
    # was read, then we have reached the end of the file.
    while line:
        if delimiter in line:
            occurences.append(line)
        line = fileStream.readline()
    #END WHILE
    #Have the file stream seek back to it's starting place
    fileStream.seek(startingPlace)
    return occurences
#END DEF

def isLessThanVersion(minVer):
    """
    This version will check the current python build's version number
    against the tuple passed in. If the version is lower than the value passed, return false
    ARGS:
        minVer:     tuple (major num, minor num), to be compared with sys.version_info. e.g. (3,0)
    RETURNS:
        None
    RAISES:
        ValueError passed minimum version is not a tuple
    """
    if type(minVer) is tuple:
        from sys import version_info
        # Comparing the version info in the sys module to the version passed
        return (version_info < minVer)
    raise ValueError("You need to pass in a tuple the compare the current version to. e.g. (3,0)")
#END DEF




# MONTH ABBR/NUM CONVERSION ----------------------------------------------------

# Found on http://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
def monthAbbrToNum(date):
    """
    This function takes an abbreviation for a month name and returns the number index
    ARGS:
        date:   String, abbreviation for a month (e.g. Jun, Oct, etc.)
    RETURNS:
        Integer, representing the month index (from 1 to 12)
    """
    return{ 'Jan' : 1, 'Feb' : 2, 'Mar' : 3,
            'Apr' : 4, 'May' : 5, 'Jun' : 6,
            'Jul' : 7, 'Aug' : 8, 'Sep' : 9,
            'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }[date]
#END DEF
def monthNumToAbbr(num):
    """
    This function takes a number index for a month and returns the name abbreviation
    ARGS:
        num:    Integer, representing the month index (from 1 to 12)
    RETURNS:
        String, abbreviation for a month (e.g. Jun, Oct, etc.)
    """
    return{ 1 : 'Jan', 2 : 'Feb', 3 : 'Mar',
            4 : 'Apr', 5 : 'May', 6 : 'Jun',
            7 : 'Jul', 8 : 'Aug', 9 : 'Sep',
            10: 'Oct', 11: 'Nov', 12: 'Dec' }[num]
#END DEF




# STATISTICAL FUNCTIONS --------------------------------------------------------

def calcArray_OutliersRemoved(array, stepsAway):
    """
    This function will take a given array, calculated the average and standard deviation,
    and then return an array that has the outliers removed, so that all elements in the list now fall
    within the specified number of standard deviations from the original average. Will also return the
    original average and standard deviation (as part of a 3 value tuple)
    ARGS:
        array:      list of values that will be used
        stepsAway:  Integer, the number of stdev "steps" away from the mean that will be used as a threshhold
    RETURNS:
        Tuple of (new array, average, stdev)
    """
    from statistics import pstdev, mean
    if not array:
        return (None, None, [])
    average = mean(array)
    stdev = pstdev(array)
    return ([val for val in array
             if (val>(average-(stepsAway*stdev))
                 and val<(average+(stepsAway*stdev))
                 )
             ],
            average, stdev
            )
#END DEF




# TEST ANALYSIS ----------------------------------------------------------------

def calcTCPThroughput(RTT, MSS=1024, Loss=0.000001):
    """
    Given a few values (RTT is required), this function will return
    the theoretical TCP Throughput on the connection from which the RTT was obtained.
    RTT must be in milliseconds
    MSS must be in bytes
    Loss must be in percent
    Returns the theoretical throughput in bits/sec.
    ARGS:
        RTT     Integer/Float, the round trip time it took to send a packet on a connection.
                Cannot be a string, None, or 0
        MSS     Integer/Float, default 1024, the maximum segment size that can be sent in the TCP connection.
                Cannot be a string, None, or 0
        Loss    Integer/Float, default 0.01, the percentage of packets that will be lost in the connection.
                Cannot be a string, None, or 0
    RETURNS:
        Integer/None    Returns None if wrong type of value was given, otherwise an Integer
    """
    for value in [RTT, MSS, Loss]:
        if (value is None) or (isinstance(value, str)):
            return None
    #END FOR
    for value in [RTT, MSS, Loss]:
        if (value == 0):
            return 0
    #END FOR
    RTT_calc = RTT / 1000.0
    MSS_calc = MSS * 8.0 / 1024.0
    Loss_calc = Loss / 100.0
    from math import sqrt
    return ( (MSS_calc / RTT_calc) / sqrt(Loss_calc) )
#END DEF

def calc_rVal_MOS(pktSum, pktCount, pktExpected, pktLost, pktFd):
    """
    This takes a few given numbers that come from determining RTT and packet loss,
    and returns the rVal and MOS as a tuple.
    ARGS:
        pktSum          Float, sum of RTT values of all pings in a Ping test
        pktCount        Float, number of pings in Ping test that did not fail
        pktExpected     Float, number of successful pings expected
        pktLost         Float, number of unsuccessful pings in a Ping test
        pktFd           Float, number of pings whose RTT was less than a given limit (150 ms)
    RETURNS:
        (rVal, MOS)     Tuple of Floats
    """
    #Doing some value checking
    for elem in [pktSum, pktCount, pktExpected, pktLost, pktFd]:
        if not isinstance(elem, float):
            raise TypeError
    #END FOR
    #Calculating the average RTT (Sum is a sum of all RTT, Count is how many)
    pktAverage = pktSum / pktCount

    #pktFd is the number of packets (i.e. pings) where the RTT was below
    # a certain threshold. We divide that by how many pings were sent (pktExpected)
    # to get a decimal representation of the ratio.
    pktFd = pktFd / pktExpected

    #Loss rate is calculate using this formula
    P_n = pktLost / pktCount
    #Loss rate of jitter buffer is calculated using this formula
    P_b = (1 - P_n) * (1 - pktFd)
    #Equipment Impairment Factor
    I_eEff = 5 + (90 * (P_n+P_b) / (P_n+P_b+10) )
    #Calculating H(x). This is either 0 or 1
    H_of_X = 0 if ((pktAverage-177.3) < 0) else 1
    #Calculating Delay Impairment Factor
    I_d = (0.024 * pktAverage) + (0.11 * (pktAverage-177.3) * H_of_X)

    #Now we can finally calculate the rValue and the MOS
    rValue = 93.2 - I_d - I_eEff
    MOS = 1 if (rValue <= 0) else ( 1 + (0.035*rValue) + (rValue * (rValue-60) * (100-rValue) * 7 * 0.000001 ) )
    #This line is for rounding off the extra numbers on the end of the MOS value.
    # We just want 1 place after the decimal
    MOS = float(round(MOS*10))/10.0
    #And now we return a tuple of the rVal and MOS value. Returned in a tuple
    # because I didn't want to use an array. Deal with it
    return [rValue, MOS]
#END DEF
